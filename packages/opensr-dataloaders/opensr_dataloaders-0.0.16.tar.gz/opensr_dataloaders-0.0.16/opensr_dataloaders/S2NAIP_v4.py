import torch
import os
import pandas as pd
import torch
import random
from einops import rearrange
from torchvision import transforms
import numpy as np
from tqdm import tqdm
from torch.utils.data import Dataset, DataLoader, WeightedRandomSampler


# Step 2: Custom Dataset Class
class S2NAIP_v4(Dataset):
    def __init__(self, csv_path, phase="train",apply_norm=False):
        
        # set properties
        self.phase = phase
        assert phase in ["train","val","test"], "Phase must be either 'train', 'val' or 'test'"
        self.apply_norm=apply_norm

        # set paths
        self.input_dir = "/data3/final_s2naip_simon/"
        self.hr_input_path = os.path.join(self.input_dir,self.phase,"HR")
        self.lr_input_path = os.path.join(self.input_dir,self.phase,"LR")
        self.degradations = ["none","gaussian","bell","sigmoid"]

        # read and clean DF
        if self.phase=="train":
            self.dataframe = pd.read_csv(csv_path)
            self.dataframe = self.dataframe.fillna(0)
            self.dataframe = self.dataframe[self.dataframe["SuperClass"]!=0]
        if self.phase=="val" or self.phase=="test":
            dfs = [[],[],[],[],[]]
            # read all files of folder into pandas
            for filename in os.listdir(self.hr_input_path):
                file_path = os.path.join( self.hr_input_path, filename)
                
                # Check if it is a file
                if os.path.isfile(file_path):
                    # Assuming the files are CSVs. For Excel, use read_excel.
                    dfs[0].append(file_path)

                    file_path_lr = os.path.join( self.lr_input_path,self.degradations[0], filename)
                    dfs[1].append(file_path_lr)

                    file_path_lr = os.path.join( self.lr_input_path,self.degradations[1], filename)
                    dfs[2].append(file_path_lr)

                    file_path_lr = os.path.join( self.lr_input_path,self.degradations[2], filename)
                    dfs[3].append(file_path_lr)

                    file_path_lr = os.path.join( self.lr_input_path,self.degradations[3], filename)
                    dfs[4].append(file_path_lr)
            df = pd.DataFrame(dfs) # convert lists to dfataframe
            df = df.T
            df.columns = ["HR"]+self.degradations
            self.dataframe = df

        # initialize sampler
        if self.phase=="train":
            self.define_sampler()
        # initialize norm
        from opensr_dataloaders.linear_transforms import linear_transform
        self.linear_transform = linear_transform
        # init albumentations
        from opensr_dataloaders.image_augmentations import init_color_transform
        self.color_transform = init_color_transform(brightness=0.5,contrast=0.5,saturation=0.5,hue=0.5)
        from opensr_dataloaders.image_augmentations import augment_bands
        self.augment_bands = augment_bands
        from opensr_dataloaders.image_augmentations import add_black_spots
        self.add_black_spots = add_black_spots
        from opensr_dataloaders.image_augmentations import other_augmentations
        self.other_augmentations = other_augmentations

    def __len__(self):
        return len(self.dataframe)
    
    def normalization(self, im, stage="norm"):
        im = im.unsqueeze(0)
        im = self.linear_transform(im,stage=stage)
        im = im.squeeze(0)
        return(im)
    
    def apply_augmentations(self,lr,hr):
        lr,hr = lr.float(),hr.float()

        # set probabilities
        smoothen_liklelihood   = 0.80 # 0.75
        jitter_liklelihood     = 0 #0.40 # 0.75
        black_spots_likelihood = 0.00

        # get random numbers
        smoothen_rand = random.uniform(0, 1)
        jitter_rand = random.uniform(0, 1)
        black_spots_rand = random.uniform(0, 1)

        # perform color jitter
        if jitter_rand<jitter_liklelihood:
            lr,hr = self.augment_bands(lr,hr,self.color_transform)

        # perform other augmentations
        lr,hr = self.other_augmentations(lr,hr)

        # perform smoothen
        if smoothen_rand<smoothen_liklelihood:
            # Define Kernel
            sigma_rand = random.uniform(0.65, 1.2)
            gaussian_blur = transforms.GaussianBlur(kernel_size=5, sigma=sigma_rand)
            # Apply the blur to the image tensor
            band_ls = []
            for band in lr:
                band = torch.unsqueeze(band,0)
                band = gaussian_blur(band)
                band = torch.squeeze(band,0)
                band_ls.append(band)
            lr = torch.stack(band_ls)
        
        if black_spots_likelihood<black_spots_rand:
            lr = self.add_black_spots(lr)
            
                
        return(lr,hr)
    
    def define_sampler(self):
        # stratiefied Sampling with weights - ideally it sums up to 1
        class_weights = {
            'Rural': 0.30,  
            'Forest': 0.25, 
            'Water': 0.05,  
            'Developed': 0.4, }
        
        # 1. clean dataset
        data = self.dataframe
        # 2. define sampler
        class_counts = data['SuperClass'].value_counts()
        base_weights = [1.0 / class_counts[i] for i in data['SuperClass'].values]
        adjusted_weights = [base_weights[i] * class_weights[class_label] for i, class_label in enumerate(data['SuperClass'].values)] 
        # 3. set sampler
        self.sampler = WeightedRandomSampler(adjusted_weights, len(adjusted_weights),replacement=True)
    
    def __getitem__(self, idx):
        # get random degradation, get input paths
        random_degradation = np.random.choice(self.degradations)
        lr_input_path = os.path.join(self.input_dir,self.phase,"LR",random_degradation)

        if self.phase=="train":
            lr_input_path = os.path.join(lr_input_path,self.dataframe.iloc[idx]["name"] + ".pt")
            hr_input_path = os.path.join(self.hr_input_path,self.dataframe.iloc[idx]["name"] + ".pt")
        if self.phase=="val":
            hr_input_path = self.dataframe.iloc[[idx]]["HR"].item()
            lr_input_path = self.dataframe.iloc[[idx]][random_degradation].item()
        if self.phase=="test":
            hr_input_path = self.dataframe.iloc[[idx]]["HR"].item()
            lr_input_path = self.dataframe.iloc[[idx]][random_degradation].item()

        # check if files exist
        if not os.path.exists(lr_input_path) or not os.path.exists(hr_input_path):
            print("WARINING: file not available.")
            print(lr_input_path,hr_input_path)

       # Load iamges from disk
        lr_image = torch.load(lr_input_path)
        hr_image = torch.load(hr_input_path)
        lr_image = lr_image.float()
        lr_image = lr_image.float()

        # bring to value range. Check since they are mixed while writing to disk is ongoing
        if hr_image.max()>10:
            hr_image = hr_image/10000
        if lr_image.max()>10:
            lr_image = lr_image/10000

        # perform augmentations
        if self.phase=="train":
            lr_image,hr_image = self.apply_augmentations(lr_image,hr_image)
        else:
            pass

        hr_image = rearrange(hr_image,"c h w -> h w c")
        lr_image = rearrange(lr_image,"c h w -> h w c")

        # return images
        return {"image":hr_image,"LR_image":lr_image}

if False:
    ds = S2NAIP_v4(phase="val",csv_path="/data3/landcover_s2naip/csvs/train_metadata_landcover.csv")
    dl = DataLoader(ds,batch_size=1,shuffle=False,num_workers=0)
    lr_means = []
    hr_means = []
    for batch in tqdm(dl):
        lr_means.append(batch["LR_image"].max().item())
        hr_means.append(batch["image"].max().item())

        if batch["LR_image"].max().item()>10 or batch["image"].max().item()>10:
            print("Unusual: ",batch["LR_image"].max().item(),batch["image"].max().item())
    


if False:
    # create objects
    ds = S2NAIP_v4(csv_path="/data3/landcover_s2naip/csvs/train_metadata_landcover.csv")
    print("Lenght: ",len(ds))
    batch = ds.__getitem__(5679)
    hr,lr = batch["image"],batch["LR_image"]
    # show lr and hr images
    import matplotlib.pyplot as plt
    from ldm.helper_functions.stretching import convention_stretch_sen2
    fig,ax = plt.subplots(1,2,figsize=(20,10))
    lr_viz,hr_viz = lr,hr
    lr_viz = ds.linear_transform(lr_viz,stage="denorm")
    hr_viz = ds.linear_transform(hr_viz,stage="denorm")
    #lr_viz,hr_viz = (lr_viz+1)/2,(hr_viz+1)/2
    hr_viz = rearrange(hr_viz,"c h w -> h w c")
    lr_viz = rearrange(lr_viz,"c h w -> h w c")
    hr_viz = convention_stretch_sen2(hr_viz)
    lr_viz = convention_stretch_sen2(lr_viz)
    ax[0].imshow(hr_viz[:,:,:3])
    ax[1].imshow(lr_viz[:,:,:3])
    plt.savefig("test.png")





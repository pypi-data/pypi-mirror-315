import torch
from torch.utils.data import Dataset, DataLoader
import mlstac
from rasterio import CRS, Affine
import os
from io import BytesIO
import numpy as np
import h5py


# Define your dataset class
class SEN2NAIPv2(Dataset):
    def __init__(self, phase="train"):        

        dataset_type = "synthetic2" # ["real","synthetic1","synthetic2"]
        base_path = "/data2/simon/"

        assert dataset_type in ["real","synthetic1","synthetic2"],"Dataset type not found. Choose from ['real','synthetic-v1','synthetic-v2']"
        self.path = os.path.join(base_path,'SEN2NAIPv2-'+dataset_type,"main.json")
        assert os.path.exists(self.path), "Dataset not found. Please check the path."
        self.dataset = mlstac.load(self.path,force=True)

        # train-test-val split
        if phase=="val":
            phase="validation"
        if "split" in self.dataset.metadata.columns:
            self.dataset.metadata = self.dataset.metadata[self.dataset.metadata["split"]==phase]
        else:
            from sklearn.model_selection import train_test_split
            # Assuming df is your pandas dataframe
            train_val, test = train_test_split(self.dataset.metadata, test_size=0.1,random_state=42)  # 80% train+val, 20% test
            train, val = train_test_split(train_val, test_size=0.10,random_state=42)  # 20% val from 80% -> 60% train, 20% val
            if phase=="train":
                self.dataset.metadata = train
            elif phase=="validation":
                self.dataset.metadata = val
            elif phase=="test":
                self.dataset.metadata = test
        self.phase=phase

        from opensr_dataloaders.linear_transform import linear_transform
        self.linear_transform = linear_transform

        print("Instanciated SEN2NAIPv2 dataset with",len(self.dataset.metadata),"datapoints for",phase)

    def __len__(self):
        return len(self.dataset.metadata)

    def get_b4(self,t):
        if t.shape[0]==3:
            average = torch.mean(t, dim=0)
            result = torch.cat((t, average.unsqueeze(0)), dim=0)
            return(result)
        else:
            return(t)

    def __getitem__(self, idx):
        datapoint = self.dataset.metadata.iloc[idx]
        lr,hr = self.get_data(datapoint)
        lr = lr.transpose(2,0,1)
        hr = hr.transpose(2,0,1)
        lr = lr[:,:128,:128]
        hr = hr[:,:512,:512]
        lr,hr = torch.tensor(lr).float(),torch.tensor(hr).float()
        lr = self.get_b4(lr)
        hr = self.get_b4(hr)
        lr = lr/10000.
        hr = hr/10000.

        apply_norm = True
        if apply_norm:
            lr,hr = lr.unsqueeze(0),hr.unsqueeze(0)
            lr = self.linear_transform(lr,stage="norm")
            hr = self.linear_transform(hr,stage="norm")
            lr,hr = lr.squeeze(0),hr.squeeze(0)

        # augmentations
        if self.phase=="train":
            pass
            #lr,hr = self.stretch_augmentation(lr,hr)
        # reshape to W,H,C
        lr = lr.permute(1,2,0)
        hr = hr.permute(1,2,0)
        return {"LR_image":lr,"image":hr}

    def get_data(self,datapoint):
        data_bytes = mlstac.get_data(dataset=datapoint,
            backend="bytes",
            save_metadata_datapoint=True,
            quiet=True)

        with BytesIO(data_bytes[0][0]) as f:
            with h5py.File(f, "r") as g:
                #metadata = eval(g.attrs["metadata"])
                lr1 = np.moveaxis(g["input"][0:4], 0, -1)
                hr1 = np.moveaxis(g["target"][0:4], 0, -1)
        lr1 = lr1.astype(np.float32)
        hr1 = hr1.astype(np.float32)

        return(lr1,hr1)

    def stretch_augmentation(self,lr,hr):
        #get rand value between 0.8 and 1.5
        rand = np.random.uniform(0.75,1.5)
        hr = hr*rand
        lr = lr*rand
        return(lr,hr)


if __name__ == "__main__":
    from omegaconf import OmegaConf
    ds = SEN2NAIPv2(phase="train")
    
    for i in range(1):
        b = ds.__getitem__(0)


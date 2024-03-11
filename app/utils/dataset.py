import os
from torchvision import datasets
import torch
from torchvision.transforms import Compose, Resize, ToTensor, Normalize
from torch.utils.data import DataLoader, Dataset, SubsetRandomSampler


class DataPreparation:
    def __init__(self, data_path=None, batch_size=32, validation_split=None, transforms=None, feature_preparation=False,
                 train_feature_dataset=None, val_feature_dataset=None):
        self.data_path = data_path
        self.batch_size = batch_size
        self.validation_split = validation_split
        self.transforms = transforms if transforms is not None else self.default_transforms()
        self.feature_preparation = feature_preparation
        if validation_split is not None:
            pass
        else:
            pass

        if train_feature_dataset and val_feature_dataset is not None:
            self.train_dataset = train_feature_dataset
            self.val_dataset = val_feature_dataset
        else:
            self.train_dataset = datasets.ImageFolder(root=os.path.join(self.data_path, 'train'),
                                                      transform=self.transforms)
            self.val_dataset = datasets.ImageFolder(root=os.path.join(self.data_path, 'val'), transform=self.transforms)

    def default_transforms(self):
        # Default transformations
        return Compose([
            Resize((224, 224)),
            ToTensor(),
            # Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
        ])

    def split_train_val_dataset(self):
        dataset = datasets.ImageFolder(root=self.data_path, transform=self.transforms)
        dataset_size = len(dataset)
        indices = list(range(dataset_size))
        split = int(torch.floor(self.validation_split * dataset_size))

        # Shuffle indices
        torch.manual_seed(42)
        torch.random.shuffle(indices)

        train_indices, val_indices = indices[split:], indices[:split]

        # Creating PT data samplers
        train_sampler = SubsetRandomSampler(train_indices)
        valid_sampler = SubsetRandomSampler(val_indices)

        # Creating data loaders
        train_loader = DataLoader(dataset, batch_size=self.batch_size, sampler=train_sampler)
        val_loader = DataLoader(dataset, batch_size=self.batch_size, sampler=valid_sampler)

        return train_loader, val_loader

    def get_classes(self):
        return len(self.train_dataset.classes)

    def prepare_data(self):
        if self.feature_preparation:
            return (self.train_dataset, self.val_dataset)

        else:
            train_loader = DataLoader(self.train_dataset, batch_size=self.batch_size, shuffle=True)
            val_loader = DataLoader(self.val_dataset, batch_size=self.batch_size, shuffle=False)
            return (train_loader, val_loader)


class TensorDataset(Dataset):
    def __init__(self, image_tensors, label_tensors):
        self.image_tensors = image_tensors
        self.label_tensors = label_tensors

    def __len__(self):
        return self.image_tensors.size(0)

    def __getitem__(self, idx):
        image = self.image_tensors[idx]
        label = self.label_tensors[idx]
        return image, label

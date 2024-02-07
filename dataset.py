from torchvision import datasets
from torchvision.transforms import Compose, Resize, ToTensor, Normalize
from torch.utils.data import DataLoader

class DataPreparation:
    def __init__(self, train_dir, val_dir, batch_size=32, transforms=None):
        self.train_dir = train_dir
        self.val_dir = val_dir
        self.batch_size = batch_size
        self.transforms = transforms if transforms is not None else self.default_transforms()

    def default_transforms(self):
        # Default transformations
        return Compose([
            Resize((224, 224)),
            ToTensor(),
            Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
        ])

    def prepare_data(self):
        # Prepare training data
        train_dataset = datasets.ImageFolder(root=self.train_dir, transform=self.transforms)
        train_loader = DataLoader(train_dataset, batch_size=self.batch_size, shuffle=True)

        # Prepare validation data
        val_dataset = datasets.ImageFolder(root=self.val_dir, transform=self.transforms)
        val_loader = DataLoader(val_dataset, batch_size=self.batch_size, shuffle=False)

        return train_loader, val_loader
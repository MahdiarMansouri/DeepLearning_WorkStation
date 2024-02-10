import torch
from skimage.exposure import exposure
from skimage.feature import hog
from torch.utils.data import Dataset, DataLoader
import numpy as np
from skimage.filters import sobel, gabor
from skimage import morphology


class FeatureExtractionDataset(Dataset):
    def __init__(self, dataset, feature_method='sobel'):
        self.dataset = dataset
        self.feature_method = feature_method

    def apply_sobel(self, image):
        # Apply Sobel filter on each channel separately and stack them
        filtered_channels = [sobel(image[i].numpy()) for i in range(image.shape[0])]
        return torch.tensor(np.stack(filtered_channels), dtype=torch.float32)

    def apply_morphology(self, image):
        # Apply morphological operation (erosion) on each channel separately and stack them
        eroded_channels = [morphology.erosion(image[i].numpy()) for i in range(image.shape[0])]
        return torch.tensor(np.stack(eroded_channels), dtype=torch.float32)

    def apply_gabor(self, image):
        # Apply Gabor filter on each channel separately and stack them
        filtered_channels = [gabor(image[i].numpy(), frequency=0.6)[0] for i in range(image.shape[0])]
        return torch.tensor(np.stack(filtered_channels), dtype=torch.float32)

    def apply_hog(self, image):
        # Apply HOG feature extraction on each channel separately and stack them
        hog_channels = []
        for i in range(image.shape[0]):
            # Extract HOG features for the single channel and rescale features
            fd, hog_channel = hog(image[i, :, :].numpy(),
                                  orientations=8,
                                  pixels_per_cell=(8, 8),
                                  cells_per_block=(1, 1),
                                  visualize=True)
            hog_channel = exposure.rescale_intensity(hog_channel, in_range=(0, 10))
            hog_channels.append(hog_channel)

        # Stack the HOG images to form a 3-channel image
        hog_image = np.stack(hog_channels, axis=0)
        return torch.tensor(hog_image, dtype=torch.float32)

    def __getitem__(self, idx):
        image, label = self.dataset[idx]

        if self.feature_method == 'sobel':
            image = self.apply_sobel(image)
        elif self.feature_method == 'morph':
            image = self.apply_morphology(image)
        elif self.feature_method == 'gabor':
            image = self.apply_gabor(image)
        elif self.feature_method == 'hog':
            image = self.apply_hog(image)
        else:
            raise ValueError(f"Unsupported feature extraction method: {self.feature_method}")

        return image, label

    def __len__(self):
        return len(self.dataset)

    def extract_features(self):
        # Iterate over the dataset and extract features
        feature_images = []
        labels = []
        for image, label in self:
            feature_images.append(image)
            labels.append(label)

        # Return a new dataset of features
        return torch.stack(feature_images), torch.tensor(labels)


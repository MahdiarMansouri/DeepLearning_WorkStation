import torchvision.models as models
import torch
from torch import nn, optim
from torchvision import datasets, transforms
from torch.utils.data import DataLoader

class PretrainedModelLoader:
    def __init__(self, model_name, pretrained=True):
        self.model_name = model_name.lower()  # todo: Ensure that input name is lowercase to match the names
        self.pretrained = pretrained
        self.model = self.get_pretrained_model()

    def get_pretrained_model(self):
        # Defining dict of classification pretrained models
        model_names = {
            'alexnet': models.alexnet,
            'convnext': models.convnext_small,
            'densenet': models.densenet121,
            'efficientnet': models.efficientnet_b0,
            'efficientnetv2': models.efficientnet_v2_s,
            'googlenet': models.googlenet,
            'inceptionv3': models.inception_v3,
            'maxvit': models.maxvit_t,
            'mnasnet': models.mnasnet1_0,
            'mobilenetv2': models.mobilenet_v2,
            'mobilenetv3': models.mobilenet_v3_large,
            'regnet': models.regnet_y_400mf,
            'resnet': models.resnet50,
            'resnext': models.resnext50_32x4d,
            'shufflenetv2': models.shufflenet_v2_x1_0,
            'squeezenet': models.squeezenet1_0,
            'swintransformer': models.swin_t,
            'vgg': models.vgg16,
            'visiontransformer': models.vit_b_16,
            'wideresnet': models.wide_resnet50_2,
        }

        if self.model_name in model_names:
            return model_names[self.model_name](pretrained=self.pretrained)
        else:
            raise ValueError(f"Model {self.model_name} is not supported or does not exist.")


class BaseModel:
    def __init__(self, model_fn, **hyperparams):
        self.model = model_fn(pretrained=hyperparams.get("pretrained", True))
        self.hyperparams = hyperparams
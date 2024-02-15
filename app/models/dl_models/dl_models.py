import json
import torchvision.models as models
import torch


class PretrainedModelLoader:
    def __init__(self):
        # Defining dict of classification pretrained models
        self.model_names = {
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


    def get_pretrained_model(self, model_name, pretrained=True):
        if model_name in self.model_names:
            return self.model_names[model_name](pretrained=pretrained)
        else:
            raise ValueError(f"Model {model_name} is not supported or does not exist.")


class BaseModel:
    def __init__(self, model_name, model_path, pretrained):
        self.name = model_name
        self.path = model_path
        self.pretrained = pretrained

    def get_model(self):
        return torch.load(self.path)

    def __repr__(self):
        return json.dumps(self.__dict__)

class Result:
    def __init__(self, model_name, epoch_nums, batch_size, input_size, pretrained, output_classes,
                 feature_extraction_method, optimizer, loss_function,  learning_rate,  result_lists):
        self.model_name = model_name
        self.epoch_nums = epoch_nums
        self.batch_size = batch_size
        self.input_size = input_size
        self.pretrained = pretrained
        self.output_classes = output_classes
        self.feature_extraction_method = feature_extraction_method
        self.optimizer = optimizer
        self.loss_function = loss_function
        self.learning_rate = learning_rate
        self.result_lists = result_lists

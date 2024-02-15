import json
import torchvision.models as models
import torch
import torch.nn as nn


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

    def get_model(self, output_classes):
        model = torch.load(self.path)
        self._modify_output_layer(model, output_classes)
        return model

    def _modify_output_layer(self, model, output_classes):
        if hasattr(model, 'fc'):
            num_features = model.fc.in_features
            model.fc = nn.Linear(num_features, output_classes)
        elif hasattr(model, 'classifier'):
            if isinstance(model.classifier, nn.Linear):
                num_features = model.classifier.in_features
                model.classifier = nn.Linear(num_features, output_classes)
            elif isinstance(model.classifier, nn.Sequential):
                num_features = model.classifier[-1].in_features
                model.classifier[-1] = nn.Linear(num_features, output_classes)
        elif hasattr(model, 'head'):
            num_features = model.head.in_features
            model.head = nn.Linear(num_features, output_classes)
        else:
            print(
                f"Warning: Output layer modification for model {self.name} is not implemented. The model architecture might need a specific adjustment.")

    def __repr__(self):
        return json.dumps(self.__dict__)


class Result:
    def __init__(self, model_name, epoch_nums, batch_size, pretrained, output_classes, feature_method, optimizer,
                 loss_function, learning_rate, train_acc_list, val_acc_list, train_loss_list, val_loss_list):
        self.model_name = model_name
        self.epoch_nums = epoch_nums
        self.batch_size = batch_size
        self.pretrained = pretrained
        self.output_classes = output_classes
        self.feature_method = feature_method
        self.optimizer = optimizer
        self.loss_function = loss_function
        self.learning_rate = learning_rate
        self.train_acc_list = train_acc_list
        self.val_acc_list = val_acc_list
        self.train_loss_list = train_loss_list
        self.val_loss_list = val_loss_list

    def __repr__(self):
        return json.dumps(self.__dict__)

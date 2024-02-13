import json
import torchvision.models as models


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
    def __init__(self, model_name, model_structure, pretrained):
        self.name = model_name
        self.structure = model_structure
        self.pretrained = pretrained

    def __repr__(self):
        return json.dumps(self.__dict__)

class Result:
    # todo: add Result entity for further process and saving to database
    # def __init__(self, model_name, epoch_nums, batch_size, Input_size, validation_split, pretrained_or_not, output_classes,
    #              feature_extraction_method, optimizer, learning_rate, regularizer, best_model_acc, result_lists):
    pass

# test
# model_loader = PretrainedModelLoader()
# for name in model_loader.model_names.keys():
#     model = model_loader.get_pretrained_model(name)
#     print(name)
#     print(model.state_dict())
#     print('0' * 300)
#
#     for param in model.state_dict():
#         model.state_dict()[param] = model.set_extra_state(0)
#         print(model.state_dict()[param])
#         time.sleep(10)
#
#     print(len(model.state_dict()))
#     print('1' * 300)
#     time.sleep(1)

#
#
# tensor([[[[ 1.1864e-01,  9.4069e-02,  9.5435e-02,  ...,  5.5822e-02,            2.1575e-02,  4.9963e-02],
# tensor([[[[ 1.1864e-01,  9.4069e-02,  9.5435e-02,  ...,  5.5822e-02,            2.1575e-02,  4.9963e-02],
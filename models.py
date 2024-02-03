import torch
import torch.nn as nn
import torchvision


class Model(nn.Module):
    def __init__(self, model_name):
        # super().__init__(Model)
        self.model_name = model_name

    def create_model(self):
        model = torchvision.models.get_model(self.model_name)
        return model

M = Model('resnet50')
model = M.create_model()
# print(param for param in model.parameters())
for child in model.children():
    print(child)
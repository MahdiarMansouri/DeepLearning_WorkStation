import torchvision


class Model:
    def __init__(self, model_name):
        self.model_name = model_name

    def create_model(self):
        model = torchvision.models.get_model(self.model_name)
        return model


M = Model('resnet50')
model = M.create_model()
print(model.fc.out_features)

for child in model.children():
    print(child)

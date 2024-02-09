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
            if self.pretrained:
                return model_names[self.model_name](pretrained=True)
            else:
                return model_names[self.model_name](pretrained=False)
        else:
            raise ValueError(f"Model {self.model_name} is not supported or does not exist.")


class BaseModel:
    def __init__(self, model_fn, **hyperparams):
        self.model = model_fn(pretrained=hyperparams.get("pretrained", True))
        self.hyperparams = hyperparams
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.model.to(self.device)

    def train(self, train_loader, val_loader=None):
        criterion = nn.CrossEntropyLoss()
        optimizer = optim.Adam(self.model.parameters(), lr=self.hyperparams.get("lr", 0.001))

        epochs = self.hyperparams.get("epochs", 10)
        for epoch in range(epochs):
            self.model.train()
            running_loss = 0.0
            for inputs, labels in train_loader:
                inputs, labels = inputs.to(self.device), labels.to(self.device)
                optimizer.zero_grad()

                outputs = self.model(inputs)
                loss = criterion(outputs, labels)
                loss.backward()
                optimizer.step()

                running_loss += loss.item()
            print(f"Epoch {epoch + 1}, Loss: {running_loss / len(train_loader)}")

            if val_loader:
                self.evaluate(val_loader)

    def evaluate(self, data_loader):
        self.model.eval()
        correct = 0
        total = 0
        with torch.no_grad():
            for inputs, labels in data_loader:
                inputs, labels = inputs.to(self.device), labels.to(self.device)
                outputs = self.model(inputs)
                _, predicted = torch.max(outputs.data, 1)
                total += labels.size(0)
                correct += (predicted == labels).sum().item()
        print(f'Accuracy: {100 * correct / total}%')

    def save_model(self, path):
        torch.save(self.model.state_dict(), path)

    def load_model(self, path):
        self.model.load_state_dict(torch.load(path))

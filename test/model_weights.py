import io
import pickle
import torch
from torchvision.models import resnet50, ResNet50_Weights

# Old weights with accuracy 76.130%
model1 = resnet50(weights=ResNet50_Weights.IMAGENET1K_V1)

# New weights with accuracy 80.858%
model2 = resnet50(weights=ResNet50_Weights.IMAGENET1K_V2)

# Best available weights (currently alias for IMAGENET1K_V2)
# Note that these weights may change across versions
model3 = resnet50(weights=ResNet50_Weights.DEFAULT)

# Strings are also supported
model4 = resnet50(pretrained=True)
model6 = resnet50()

# No weights - random initialization
model5 = resnet50(weights=None)


model_list = [model1, model2, model3, model4, model5, model6]

for i, name in enumerate(model_list):
    # buffer = io.BytesIO()
    # torch.save(name, buffer)
    # weights_bytes = buffer.getvalue()
    with open(f'model{i+1} weights', 'wb') as f:
        model_weights = name.state_dict()
        for param in model_weights:
            model_weights[param] = None
        f.write(pickle.dumps(name.state_dict()))
    with open(f'model{i+1}', 'wb') as f:
        f.write(pickle.dumps(name))

torch.save(model1.state_dict(), 'model1.pth')
torch.save(model2.state_dict(), 'model2.pth')
torch.save(model3.state_dict(), 'model3.pth')
torch.save(model4.state_dict(), 'model4.pth')
torch.save(model5.state_dict(), 'model5.pth')
torch.save(model5.state_dict(), 'model6.pth')


# Load the state dicts of two models
state_dict_with_weights = pickle.loads('model4')
state_dict_without_weights = pickle.loads('model1')

# Compare the state dicts
for ((key_with, param_with), (key_without, param_without)) in zip(state_dict_with_weights.items(), state_dict_without_weights.items()):
    if not torch.equal(param_with, param_without):
        print(f"Difference found in parameter: {key_with}")

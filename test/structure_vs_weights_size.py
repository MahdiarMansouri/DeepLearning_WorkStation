import torch
import os

# Initialize the model without pretrained weights
model = torch.hub.load('pytorch/vision:v0.6.0', 'resnet50', pretrained=False)

# Save the full state dictionary with weights and biases
torch.save(model.state_dict(), 'full_state_dict.pth')

# Calculate the file size of the full state dictionary
full_state_size = os.path.getsize('full_state_dict.pth')

# Extract and save only the weights and biases
weights_only = {k: v for k, v in model.state_dict().items() if 'weight' in k or 'bias' in k}
torch.save(weights_only, 'weights_only.pth')

# Calculate the file size of the weights-only file
weights_only_size = os.path.getsize('weights_only.pth')

# The architecture-only representation is not straightforward to obtain since PyTorch does not store
# this separately. As an approximation, you could consider the number of parameters and the structure
# of layers (excluding the actual weight values).

# Calculate the file size difference
size_difference = full_state_size - weights_only_size

print(f"Full state dictionary size: {full_state_size} bytes")
print(f"Weights-only size: {weights_only_size} bytes")
print(f"Size difference (approximate architecture size): {size_difference} bytes")

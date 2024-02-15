import torch
import torch.nn as nn


def evaluate_model(model, data_loader, criterion=nn.CrossEntropyLoss(), device='cpu'):
    model.eval()
    total_loss = 0.0
    correct_predictions = 0
    total = 0

    with torch.no_grad():
        for inputs, labels in data_loader:
            inputs, labels = inputs.to(device), labels.to(device)
            outputs = model(inputs)
            loss = criterion(outputs, labels)
            total_loss += loss.item()
            _, predicted = torch.max(outputs.data, 1)
            total += labels.size(0)
            correct_predictions += (predicted == labels).sum().item()

    val_loss = total_loss / len(data_loader)
    val_accuracy = correct_predictions / total
    return val_loss, val_accuracy

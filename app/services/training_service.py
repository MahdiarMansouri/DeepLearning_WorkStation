import torch
from torch import nn, optim
from torch.utils.data import DataLoader

def train_model(model, train_loader, val_loader=None, epochs=10, learning_rate=0.001, device='cuda'):
    """
    Trains a given model with the provided dataset.

    Parameters:
    - model: The neural network model to train.
    - train_loader: DataLoader for training data.
    - val_loader: DataLoader for validation data (optional).
    - epochs: Number of epochs to train for.
    - learning_rate: Learning rate for the optimizer.
    - device: Device to train on ('cuda' or 'cpu').

    Returns:
    - model: The trained model.
    """

    model.to(device)
    criterion = nn.CrossEntropyLoss()
    optimizer = optim.Adam(model.parameters(), lr=learning_rate)

    for epoch in range(epochs):
        model.train()
        running_loss = 0.0
        for inputs, labels in train_loader:
            inputs, labels = inputs.to(device), labels.to(device)

            optimizer.zero_grad()

            outputs = model(inputs)
            loss = criterion(outputs, labels)
            loss.backward()
            optimizer.step()

            running_loss += loss.item()

        if val_loader:
            val_loss, val_acc = evaluate_model(model, val_loader, device)
            print(f'Epoch {epoch+1}, Loss: {running_loss/len(train_loader)}, Val Loss: {val_loss}, Val Acc: {val_acc}')
        else:
            print(f'Epoch {epoch+1}, Loss: {running_loss/len(train_loader)}')

    return model

def evaluate_model(model, data_loader, device='cuda'):
    """
    Evaluates the model on the validation dataset.

    Parameters:
    - model: The neural network model to evaluate.
    - data_loader: DataLoader for the dataset to evaluate on.
    - device: Device to evaluate on ('cuda' or 'cpu').

    Returns:
    - val_loss: Average loss on the validation dataset.
    - val_accuracy: Accuracy on the validation dataset.
    """
    model.eval()
    criterion = nn.CrossEntropyLoss()
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

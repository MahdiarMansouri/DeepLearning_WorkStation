import torch
from easydict import EasyDict
from torch import nn, optim
from torch.utils.data import DataLoader


def train_model(model, train_loader, val_loader=None, epochs=10, learning_rate=0.001, optimizer='adam',
                criterion=nn.CrossEntropyLoss(), device='cpu'):
    model.to(device)
    if optimizer == 'adam':
        optimizer = optim.Adam(model.parameters(), lr=learning_rate)
    acc_list = EasyDict({'train': [], 'val': []})
    loss_list = EasyDict({'train': [], 'val': []})

    for epoch in range(epochs):
        model.train()
        running_loss = 0.0
        correct_predictions = 0
        total_samples = 0

        for inputs, labels in train_loader:
            inputs, labels = inputs.to(device), labels.to(device)

            optimizer.zero_grad()

            outputs = model(inputs)
            loss = criterion(outputs, labels)
            loss.backward()
            optimizer.step()

            running_loss += loss.item()
            _, predicted = torch.max(outputs.data, 1)
            total_samples += labels.size(0)
            correct_predictions += (predicted == labels).sum().item()

        train_loss = running_loss / len(train_loader)
        train_accuracy = correct_predictions / total_samples
        loss_list.train.append(train_loss)
        acc_list.train.append(train_accuracy)

        if val_loader:
            val_loss, val_acc = evaluate_model(model, val_loader, criterion, device)
            loss_list.val.append(val_loss)
            acc_list.val.append(val_acc)
            print(
                f'Epoch {epoch + 1}, Train Loss: {train_loss}, Train Acc: {train_accuracy}, Val Loss: {val_loss}, Val Acc: {val_acc}')
        else:
            print(f'Epoch {epoch + 1}, Train Loss: {train_loss}, Train Acc: {train_accuracy}')

    return model, loss_list, acc_list


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

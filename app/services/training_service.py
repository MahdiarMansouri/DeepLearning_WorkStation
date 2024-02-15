import torch
from easydict import EasyDict
from torch import nn, optim
from evaluating_service import evaluate_model


def train_model(model, train_loader, val_loader=None, epochs=10, learning_rate=0.001, optimizer='adam',
                criterion=nn.CrossEntropyLoss(), device='cpu'):
    model.to(device)
    if optimizer == 'adam':
        optimizer = optim.Adam(model.parameters(), lr=learning_rate)
    acc_lists = EasyDict({'train': [], 'val': []})
    loss_lists = EasyDict({'train': [], 'val': []})

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
        loss_lists.train.append(train_loss)
        acc_lists.train.append(train_accuracy)

        if val_loader:
            val_loss, val_acc = evaluate_model(model, val_loader, criterion, device)
            loss_lists.val.append(val_loss)
            acc_lists.val.append(val_acc)
            print(
                f'Epoch {epoch + 1}, Train Loss: {train_loss}, Train Acc: {train_accuracy}, Val Loss: {val_loss}, Val Acc: {val_acc}')
        else:
            print(f'Epoch {epoch + 1}, Train Loss: {train_loss}, Train Acc: {train_accuracy}')

    return model, loss_lists, acc_lists

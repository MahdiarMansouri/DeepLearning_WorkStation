from datetime import datetime

import torch
from easydict import EasyDict
from torch import nn, optim

class Trainer:
    def __init__(self, model, train_loader, val_loader=None, epochs=10, learning_rate=0.001, optimizer='adam',
                criterion='CrossEntropy', device='cpu'):
        self.model = model
        self.train_loader = train_loader
        self.val_loader = val_loader
        self.epochs = epochs
        self.learning_rate = learning_rate
        self.optimizer = optimizer
        self.criterion = criterion
        self.device = device

    def train_model(self):

        self.model.to(self.device)

        if self.criterion == 'CrossEntropy':
            self.criterion = nn.CrossEntropyLoss()

        if self.optimizer == 'adam':
            optimizer = optim.Adam(self.model.parameters(), lr=self.learning_rate)

        acc_lists = EasyDict({'train': [], 'val': []})
        loss_lists = EasyDict({'train': [], 'val': []})

        for epoch in range(self.epochs):
            s0 = datetime.now()
            self.model.train()
            running_loss = 0.0
            correct_predictions = 0
            total_samples = 0

            for inputs, labels in self.train_loader:
                inputs, labels = inputs.to(self.device), labels.to(self.device)

                optimizer.zero_grad()

                outputs = self.model(inputs)
                loss = self.criterion(outputs, labels)
                loss.backward()
                optimizer.step()

                running_loss += loss.item()
                _, predicted = torch.max(outputs.data, 1)
                total_samples += labels.size(0)
                correct_predictions += (predicted == labels).sum().item()

            train_loss = running_loss / len(self.train_loader)
            train_accuracy = correct_predictions / total_samples
            loss_lists.train.append(train_loss)
            acc_lists.train.append(train_accuracy)

            if self.val_loader:
                val_loss, val_acc = self.evaluate_model()
                loss_lists.val.append(val_loss)
                acc_lists.val.append(val_acc)
                epoch_timing = datetime.now() - s0
                print(
                    f'Epoch {epoch + 1} => Train Loss: {train_loss:.4f} | Train Acc: {train_accuracy:.4f} | Val Loss: {val_loss:.4f} | Val Acc: {val_acc:.4f} | time: {epoch_timing.seconds:.2f}')
            else:
                print(f'Epoch {epoch + 1} => Train Loss: {train_loss:.3f}, Train Acc: {train_accuracy:.3f}')

        return self.model, loss_lists, acc_lists

    def evaluate_model(self):
        self.model.eval()
        total_loss = 0.0
        correct_predictions = 0
        total = 0

        with torch.no_grad():
            for inputs, labels in self.val_loader:
                inputs, labels = inputs.to(self.device), labels.to(self.device)
                outputs = self.model(inputs)
                loss = self.criterion(outputs, labels)
                total_loss += loss.item()
                _, predicted = torch.max(outputs.data, 1)
                total += labels.size(0)
                correct_predictions += (predicted == labels).sum().item()

        val_loss = total_loss / len(self.val_loader)
        val_accuracy = correct_predictions / total
        return val_loss, val_accuracy


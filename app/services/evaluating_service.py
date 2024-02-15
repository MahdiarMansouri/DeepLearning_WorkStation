import torch

class Evaluator:
    def __init__(self, model, data_loader, criterion, device='cpu'):
        self.model = model
        self.data_loader = data_loader
        self.criterion = criterion
        self.device = device

    def evaluate_model(self):
        self.model.eval()
        total_loss = 0.0
        correct_predictions = 0
        total = 0

        with torch.no_grad():
            for inputs, labels in self.data_loader:
                inputs, labels = inputs.to(self.device), labels.to(self.device)
                outputs = self.model(inputs)
                loss = self.criterion(outputs, labels)
                total_loss += loss.item()
                _, predicted = torch.max(outputs.data, 1)
                total += labels.size(0)
                correct_predictions += (predicted == labels).sum().item()

        val_loss = total_loss / len(self.data_loader)
        val_accuracy = correct_predictions / total
        return val_loss, val_accuracy

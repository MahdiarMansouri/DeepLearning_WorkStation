from app.models.db_models.database_model import ModelDA
from app.models.dl_models.dl_models import BaseModel, Result
from app.services.training_service import Trainer
from app.utils.dataset import DataPreparation, TensorDataset
from app.utils.preprocessing import FeatureExtractionDataset
import torch
from datetime import datetime


class PipelineRunner:
    def __init__(self, data_path, dataset_name, batch_size, feature_method, model_name, pretrained, epoch_nums, optimizer,
                 learning_rate, loss_func):
        self.data_path = data_path
        self.dataset_name = dataset_name
        self.batch_size = batch_size
        self.feature_method = feature_method
        self.model_name = model_name
        self.pretrained = pretrained
        self.epoch_nums = epoch_nums
        self.optimizer = optimizer
        self.learning_rate = learning_rate
        self.loss_func = loss_func

    def data_preparation(self):
        if self.feature_method is not None:
            data_preparation = DataPreparation(data_path=self.data_path, feature_preparation=True)
            self.output_classes = data_preparation.get_classes()
            datasets = data_preparation.prepare_data()
            feature_images = []
            feature_labels = []
            for dataset in datasets:
                preprocessor = FeatureExtractionDataset(dataset, self.feature_method)
                images, labels = preprocessor.extract_features()
                feature_labels.append(labels)
                feature_images.append(images)
            train_feature_dataset = TensorDataset(feature_images[0], feature_labels[0])
            val_feature_dataset = TensorDataset(feature_images[1], feature_labels[1])
            feature_data_preparation = DataPreparation(batch_size=self.batch_size,
                                                       train_feature_dataset=train_feature_dataset,
                                                       val_feature_dataset=val_feature_dataset)
            self.dataloaders = feature_data_preparation.prepare_data()
        else:
            data_preparation = DataPreparation(data_path=self.data_path, batch_size=self.batch_size)
            self.dataloaders = data_preparation.prepare_data()
            self.output_classes = data_preparation.get_classes()

    def define_model(self):
        model_da = ModelDA()
        model = model_da.find_by_model_name_pretrained(self.model_name, 1 if self.pretrained else 0)
        model = BaseModel(*model)
        self.model = model.get_model(self.output_classes)

    def train_model(self):
        train_loader, val_loader = self.dataloaders
        device = torch.device('cuda:0' if torch.cuda.is_available() else 'cpu')
        trainer = Trainer(self.model, train_loader, val_loader, self.epoch_nums, self.learning_rate, self.optimizer,
                          self.loss_func, device)
        self.model, self.loss_lists, self.acc_lists = trainer.train_model()

    def run(self):
        s0 = datetime.now()
        self.data_preparation()
        self.define_model()
        self.train_model()
        delta_time = datetime.now() - s0
        self.running_time = delta_time.seconds / 60

    def get_results(self):
        result = Result(self.model_name, self.dataset_name, self.epoch_nums, self.batch_size, self.pretrained, self.output_classes,
                        self.feature_method, self.optimizer, self.loss_func, self.learning_rate, self.acc_lists.train,
                        self.acc_lists.val, self.loss_lists.train, self.loss_lists.val, self.running_time)
        return result

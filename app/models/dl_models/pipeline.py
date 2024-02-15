from app.models.db_models.database_model import ModelDA
from app.services.training_service import Trainer
from app.utils.dataset import DataPreparation
from app.utils.preprocessing import FeatureExtractionDataset
import torch


class PipelineRunner:
    def __init__(self, data_path, batch_size, feature_method, model_name, pretrained, epoch_nums, optimizer,
                 learning_rate, loss_func):
        self.data_path = data_path
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
            datasets = data_preparation.prepare_data()
            feature_datasets = []
            for dataset in datasets:
                preprocessor = FeatureExtractionDataset(dataset, self.feature_method)
                feature_dataset = preprocessor.extract_features()
                feature_datasets.append(feature_dataset)
            feature_data_preparation = DataPreparation(batch_size=self.batch_size,
                                                       train_feature_dataset=feature_datasets[0],
                                                       val_feature_dataset=feature_datasets[1])
            self.dataloaders, self.output_classes = feature_data_preparation.prepare_data()
        else:
            data_preparation = DataPreparation(data_path=self.data_path, batch_size=self.batch_size)
            self.dataloaders, self.output_classes = data_preparation.prepare_data()


    def define_model(self):
        model_da = ModelDA()
        model = model_da.find_by_model_name(self.model_name)
        self.model = model.get_model(self.output_classes)

    def train_model(self):
        train_loader, val_loader = self.dataloaders
        device = torch.device('cuda:0' if torch.cuda.is_available() else 'cpu')
        trainer = Trainer(self.model, train_loader, val_loader, self.epoch_nums, self.learning_rate, self.optimizer,
                          self.loss_func, device)
        self.model, self.loss_lists, self.acc_lists = trainer.train_model()

    def run(self):
        self.data_preparation()
        self.define_model()
        self.train_model()

# Example of defining different pipelines
# pipeline1 = PipelineRunner(
#     FeatureExtractionDataset(dataset, method=None)
#     DataLoader(dataset="Dataset1"),
#     Model(architecture="Architecture1"),
#     Trainer(model="Model1", data_loader="DataLoader1"),
#     Evaluator(model="Model1", data_loader="DataLoader1")
# )
#
# pipeline2 = PipelineRunner(
#     DataLoader(dataset="Dataset2"),
#     Model(architecture="Architecture2"),
#     Trainer(model="Model2", data_loader="DataLoader2"),
#     Evaluator(model="Model2", data_loader="DataLoader2")
# )
#
# pipelines = [pipeline1, pipeline2]


# for pipeline in pipelines:
#     pipeline.run()

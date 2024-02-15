class PipelineRunner:
    def __init__(self, data_preparation, feature_extraction_method, model, trainer, evaluator):
        self.data_preparation = data_preparation
        self.feature_extraction_method = feature_extraction_method
        self.model = model
        self.trainer = trainer
        self.evaluator = evaluator

    def run(self):
        self.data_loader.load_data()
        self.model.build_model()
        self.trainer.train()
        self.evaluator.evaluate()
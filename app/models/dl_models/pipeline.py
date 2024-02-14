class PipelineRunner:
    def __init__(self, data_loader, model, trainer, evaluator):
        self.data_loader = data_loader
        self.model = model
        self.trainer = trainer
        self.evaluator = evaluator

    def run(self):
        self.data_loader.load_data()
        self.model.build_model()
        self.trainer.train()
        self.evaluator.evaluate()
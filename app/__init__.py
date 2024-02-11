import pickle
import time
from app.models.db_models.database_model import ModelDA
from app.models.dl_models.dl_models import PretrainedModelLoader, BaseModel


def initialize_models_in_db():
    # Instantiate the data access and model loader classes
    model_da = ModelDA()
    model_loader = PretrainedModelLoader()

    # Check database connection
    if not model_da.check_connection():
        print("Failed to connect to the database. Exiting.")
        return

    model_da.connect()
    # Iterate over all the models and save them to the database
    for model_name in model_loader.model_names.keys():
        time.sleep(1)
        print(f"Processing {model_name} model...")

        try:
            # Load the pretrained model
            model = model_loader.get_pretrained_model(model_name, pretrained=True)

            # Serialize the model weights to binary
            weights_binary = pickle.dumps(model.state_dict())

            # Remove the weights from the model
            model_weights = model.state_dict()
            for param in model_weights:
                model_weights[param] = None

            # Serialize the model structure to binary
            model_structure_binary = pickle.dumps(model)

            # Create a BaseModel instance
            base_model = BaseModel(model_name, model_structure_binary, weights_binary)

            # Save the model structure and weights to the database
            model_da.save_model_to_db(base_model)

            print(f"The model structure and weights for {model_name} have been saved to database.")

        except Exception as e:
            print(f"An error occurred while processing {model_name}: {str(e)}")

    model_da.disconnect(commit=True)
initialize_models_in_db()

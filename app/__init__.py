import os
import torch
import time
from app.models.db_models.database_model import ModelDA
from app.models.dl_models.dl_models import PretrainedModelLoader, BaseModel


def initialize_models_in_db():
    # Define the directory where models will be saved
    models_directory = "model_files"
    os.makedirs(models_directory, exist_ok=True)

    # Create the data access and model loader objects
    model_da = ModelDA()
    model_loader = PretrainedModelLoader()

    # Check database connection
    if not model_da.check_connection():
        print("Failed to connect to the database. Exiting.")
        return

    # Loop for loading pretrained and random weights in each model
    for pretrained_flag in [True, False]:
        # Iterate over all the models and save them to the directory
        for model_name in model_loader.model_names.keys():
            print('__' * 50)
            # time.sleep(3)
            print(f"Checking for the presence of {model_name} model in the database...")

            # Check if the model file path already exists in the database
            check_model = model_da.find_by_model_name(model_name)
            if check_model and check_model.pretrained == (1 if pretrained_flag else 0):
                print(f"Model {model_name} already exists in the database. Skipping download and save.")
                continue

            print(f"Model {model_name} does not exist in the database. Processing...")

            try:
                # Load the pretrained model
                model = model_loader.get_pretrained_model(model_name, pretrained=pretrained_flag)

                # Set the file name and path where the model will be saved
                model_filename = f"{model_name}_{'pretrained' if pretrained_flag else 'random'}.pth"
                model_filepath = os.path.join(models_directory, model_filename)

                # Save the model to the specified directory
                torch.save(model, model_filepath)

                # Set pretrained flag as TINYINT of 1 & 0 for saving in database
                pretrained_flag_db = 1 if pretrained_flag else 0

                # Save the model name, file path, and pretrained flag to the database
                model_loaded = BaseModel(model_name, model_filepath, pretrained_flag_db)
                model_da.save_model_to_db(model_loaded)

                print(f"The {model_name} information has been saved to the database.")

            except Exception as e:
                print(f"An error occurred while processing {model_name}: {str(e)}")


if __name__ == '__main__':
    initialize_models_in_db()

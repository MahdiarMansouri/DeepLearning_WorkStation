import pickle
import time
from app.models.db_models.database_model import ModelDA
from app.models.dl_models.dl_models import PretrainedModelLoader, BaseModel


def initialize_models_in_db():
    # Create the data access and model loader objects
    model_da = ModelDA()
    model_loader = PretrainedModelLoader()

    # Check database connection
    if not model_da.check_connection():
        print("Failed to connect to the database. Exiting.")
        return

    # Connect to database for saving models
    # model_da.connect()

    # For loop for loading pretrained and random weights in each models
    for pretrained_flag in [True, False]:

        # Iterate over all the models and save them to the database
        for model_name in model_loader.model_names.keys():
            print('__' * 50)
            time.sleep(3)
            print(f"Checking for the presence of {model_name} model in the database...")

            # Check if the model already exists in the database
            check_model = model_da.find_by_model_name(model_name)
            if check_model:
                if check_model.pretrained == pretrained_flag:
                    print(f"Model {model_name} already exists in the database. Skipping download and save.")
                    continue

            print(f"Model {model_name} does not exist in the database. Processing...")

            try:
                # Load the pretrained model
                model = model_loader.get_pretrained_model(model_name, pretrained=pretrained_flag)

                # Serialize the entire model to binary
                model_structure_binary = pickle.dumps(model)

                # Set pretrained flag as TINYINT of 1 & 0 for saving in database
                if pretrained_flag == True:
                    pretrained_flag = 1
                else:
                    pretrained_flag = 0

                # Save the model name, structure, and pretrained flag to the database
                model_loaded = BaseModel(model_name, model_structure_binary, pretrained_flag)
                model_da.save_model_to_db(model_loaded)

                print(f"The entire structure for {model_name} has been saved to the database.")

            except Exception as e:
                print(f"An error occurred while processing {model_name}: {str(e)}")

    # model_da.disconnect(commit=True)


initialize_models_in_db()

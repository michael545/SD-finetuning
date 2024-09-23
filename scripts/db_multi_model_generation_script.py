import os
import yaml
import requests
from pathlib import Path

def load_config(config_path):
    with open(config_path, 'r') as file:
        return yaml.safe_load(file)

def create_dreambooth_model(api_url, params):
    response = requests.post(f"{api_url}/dreambooth/createModel", json=params)
    if response.status_code == 200:
        print(f"Model '{params['model_name']}' created successfully.")
    else:
        print(f"Error creating model '{params['model_name']}': {response.text}")

def main():
    config = load_config('C:\Users\umzg\Documents\Projektil\skripte\SD-finetuning\scripts\db_model_generator.yaml')
    api_url = config['api_url']
    base_model = config['base_model']
    output_dir = config['output_dir']
    
    # Ensure output directory exists
    Path(output_dir).mkdir(parents=True, exist_ok=True)

    # Iterate through the folder of folders
    for folder in os.listdir(config['data_dir']):
        folder_path = os.path.join(config['data_dir'], folder)
        if os.path.isdir(folder_path):
            # Use the folder name as the model name and instance prompt
            model_name = f"{base_model}_{folder}"
            instance_prompt = folder

            # Prepare the parameters for this model
            params = {
                "model_name": model_name,
                "base_model": base_model,
                "instance_prompt": instance_prompt,
                "class_prompt": config['class_prompt'],
                "instance_data_dir": folder_path,
                "output_dir": os.path.join(output_dir, model_name),
                "train_batch_size": config['train_batch_size'],
                "learning_rate": config['learning_rate'],
                "max_train_steps": config['max_train_steps'],
                "num_class_images": config['num_class_images'],
                "use_8bit_adam": config['use_8bit_adam'],
                "mixed_precision": config['mixed_precision'],
                "prior_loss_weight": config['prior_loss_weight']
            }

            # Create the Dreambooth model
            create_dreambooth_model(api_url, params)

if __name__ == "__main__":
    main()
import subprocess
import sys
import os
import yaml


def setup():
    install_cmds = [
        [sys.executable, '-m', 'pip', 'install', '--upgrade', 'pip'],
        [sys.executable, '-m', 'pip', 'install', 'urllib3==1.26.6'],
        [sys.executable, '-m', 'pip', 'install', 'transformers==4.30.2'],
        [sys.executable, '-m', 'pip', 'install', 'gradio==3.35.2'],
        [sys.executable, '-m', 'pip', 'install', 'open_clip_torch==2.20.0'],
        [sys.executable, '-m', 'pip', 'install', 'clip-interrogator==0.6.0'],
        [sys.executable, '-m', 'pip', 'install', 'Pillow==9.5.0'],
        [sys.executable, '-m', 'pip', 'install', 'tqdm==4.65.0'],
    ]
    for cmd in install_cmds:
        print(f"Running: {' '.join(cmd)}")
        result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        print(result.stdout.decode('utf-8'))
        print(result.stderr.decode('utf-8'))

def main():
    #setup() # cep poganjas prvic odkomentiraj, da se ti vse namesti

    # pazi ce je ze importano
    from PIL import Image
    from tqdm import tqdm
    from clip_interrogator import Config, Interrogator

    def sanitize_for_filename(prompt: str, max_len: int) -> str:
        name = "".join(c for c in prompt if (c.isalnum() or c in ",._-! "))
        name = name.strip()[:(max_len-4)]  # extra presledek za extension
        return name

    def image_to_prompt(image, ci):
        image = image.convert('RGB')
        return ci.interrogate(image)


    with open("config.yaml", 'r') as file:
        config_file = yaml.safe_load(file)

    caption_model_name = config_file.get('caption_model_name')
    clip_model_name = config_file.get('clip_model_name')
    device = config_file.get('device')
    source_folder = config_file.get('source_folder')
    destination_folder = config_file.get('destination_folder')
    max_filename_len = config_file.get('max_filename_len')

   
    print(f"Caption Model: {caption_model_name}")
    print(f"Clip Model: {clip_model_name}")
    print(f"Device: {device}")
    print(f"Source Folder: {source_folder}")
    print(f"Destination Folder: {destination_folder}")
    print(f"Max Filename Length: {max_filename_len}")

    config_file = None


    config = Config()
    config.clip_model_name = clip_model_name
    config.caption_model_name = caption_model_name
    config.quiet = True
    config.device = device
    ci = Interrogator(config)



    if not os.path.exists(destination_folder):
        os.makedirs(destination_folder)

    files = [f for f in os.listdir(source_folder) if f.lower().endswith(('.jpg', '.jpeg', '.png', '.gif'))]

    for file in tqdm(files, desc='Renaming and moving images'):
        print(f"Procesiram sliko: {file}")
        image_path = os.path.join(source_folder, file)
        image = Image.open(image_path).convert('RGB')
        print("slika odprta in convertana RGB")
        
        prompt = image_to_prompt(image, ci)
        print(f"Prompt generiran: {prompt}")
        
        new_name = sanitize_for_filename(prompt, max_filename_len)
        print(f"Sanitized ime datoteke: {new_name}")
        
        ext = os.path.splitext(file)[1]
        new_filename = f"{new_name}{ext}"
        
        counter = 1
        while os.path.exists(os.path.join(destination_folder, new_filename)):
            new_filename = f"{new_name}_{counter}{ext}"
            counter += 1
        
        new_path = os.path.join(destination_folder, new_filename)
        os.rename(image_path, new_path)
        print(f"preimenovano in premaknjeno v: {new_path}")

    print(f"\nPreimenoval in premaknil {len(files)} slik v {destination_folder}")



if __name__ == "__main__":
    main()
import subprocess
import os

def setup():
    install_cmds = [
        ['pip', 'install', 'gradio'],
        ['pip', 'install', 'open_clip_torch'],
        ['pip', 'install', 'clip-interrogator'],
        ['pip', 'install', 'Pillow'],
        ['pip', 'install', 'tqdm'],
    ]
    for cmd in install_cmds:
        print(subprocess.run(cmd, stdout=subprocess.PIPE).stdout.decode('utf-8'))

def main():
    setup()

    # safe import
    from PIL import Image
    from tqdm import tqdm
    from clip_interrogator import Config, Interrogator

    def sanitize_for_filename(prompt: str, max_len: int) -> str:
        name = "".join(c for c in prompt if (c.isalnum() or c in ",._-! "))
        name = name.strip()[:(max_len-4)]  # extra space for extension
        return name

    def image_to_prompt(image, ci):
        image = image.convert('RGB')
        return ci.interrogate(image)

    caption_model_name = 'blip-large'
    clip_model_name = 'ViT-H-14/laion2b_s32b_b79k'

    config = Config()
    config.clip_model_name = clip_model_name
    config.caption_model_name = caption_model_name
    config.quiet = True
    ci = Interrogator(config)

    source_folder = input("vnesi pot do slik: ")
    destination_folder = input("vnesi pot do mape kjer bodo preimenovane slike: ")
    max_filename_len = 128

    if not os.path.exists(destination_folder):
        os.makedirs(destination_folder)

    files = [f for f in os.listdir(source_folder) if f.lower().endswith(('.jpg', '.jpeg', '.png', '.gif'))]

    for file in tqdm(files, desc='Renaming and moving images'):
        image_path = os.path.join(source_folder, file)
        image = Image.open(image_path).convert('RGB')
        
        prompt = image_to_prompt(image, ci)
        new_name = sanitize_for_filename(prompt, max_filename_len)
        
        ext = os.path.splitext(file)[1]
        new_filename = f"{new_name}{ext}"
        
        # Ensure unique filename
        counter = 1
        while os.path.exists(os.path.join(destination_folder, new_filename)):
            new_filename = f"{new_name}_{counter}{ext}"
            counter += 1
        
        new_path = os.path.join(destination_folder, new_filename)
        os.rename(image_path, new_path)

    print(f"\nRenamed and moved {len(files)} images to {destination_folder}")

if __name__ == "__main__":
    main()
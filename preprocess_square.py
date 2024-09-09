import os
import glob
from PIL import Image

def process_images(folder_name, text_prompt, token_name, resolution):
    # Validate input folder exists 
    if not os.path.exists(folder_name):
        print(f"The folder {folder_name} does not exist.")
        return
    
    # Create output folder
    output_folder = folder_name + "_processed_" + str(resolution)
    os.makedirs(output_folder, exist_ok=True)

    # Enumerate and process each PNG file
    for idx, png_file in enumerate(glob.glob(os.path.join(folder_name, "*.png")), 1):
        # Open and resize image
        with Image.open(png_file) as im:
            im_resized = im.resize((resolution, resolution))
        
        # Generate new filename and save resized image
        new_filename = f"{idx:05d}@{os.path.basename(png_file).split('.')[0]} in style of {token_name}.png"
        im_resized.save(os.path.join(output_folder, new_filename))
        
        # Create corresponding .txt file
        txt_content = f"{text_prompt}, {os.path.basename(png_file).split('.')[0]}, in style of {token_name}"
        with open(os.path.join(output_folder, new_filename.replace(".png", ".txt")), "w") as txt_file:
            txt_file.write(txt_content)

# Example usage
process_images("SELO_ROTUNDA surove\\ucni podatki", "", "rtsl", 512)

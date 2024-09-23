import os
import glob
from PIL import Image

extensions = ('.png', '.jpg', '.jpeg')

def process_images_in_subfolders(base_folder, text_prompt, token_name, resolution):
    # Iterate over each folder inside the base folder
    for folder_name in glob.glob(os.path.join(base_folder, "*")):
        if os.path.isdir(folder_name):
            
            if not os.path.exists(folder_name):
                print(f"The folder {folder_name} does not exist.")
                continue
            
            # Create output folder inside the current folder
            output_folder = os.path.join(folder_name, f"{os.path.basename(folder_name)}_processed_{resolution}")
            os.makedirs(output_folder, exist_ok=True)
            
            # Enumerate and process each PNG file in the current folder
            for idx, png_file in enumerate(glob.glob(os.path.join(folder_name, "*.png")), 1):
                # Open and resize image
                with Image.open(png_file) as im:
                    im_resized = im.resize((resolution, resolution))
                
                # Generate new filename and save resized image
                new_filename = f"{idx:05d}@{os.path.basename(png_file).split('.')[0]} in style of {token_name}.png"
                im_resized.save(os.path.join(output_folder, new_filename))
                
                # Create corresponding .txt file
                txt_content = f"{text_prompt} {os.path.basename(png_file).split('.')[0]}{token_name}"
                with open(os.path.join(output_folder, new_filename.replace(".png", ".txt")), "w") as txt_file:
                    txt_file.write(txt_content)
            for filename in os.listdir(folder_name):
                file_path = os.path.join(folder_name, filename)
    
            # Check if the file has the correct extension and if it's a file (not a directory)
                if os.path.isfile(file_path) and filename.lower().endswith(extensions):
                    try:
                        os.remove(file_path)
                        print(f"Deleted: {file_path}")
                    except Exception as e:
                        print(f"Error deleting {file_path}: {e}")
                    

# Example usage
base_folder = r"C:\Users\umzg\Documents\Projektil\kohya_training_folder"
process_images_in_subfolders(base_folder, "", "", 1024)

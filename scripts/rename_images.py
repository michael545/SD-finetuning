import os

def convert_to_utf8(file_path):
    """Convert a file to UTF-8 encoding."""
    try:
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
        # Rewrite the file with UTF-8 encoding
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Converted {file_path} to UTF-8")
    except Exception as e:
        print(f"Failed to convert {file_path}: {e}")

def rename_files(directory):
    # Supported file extensions
    file_extensions = ('.png', '.txt', '.npz')

    # Get a list of all files with supported extensions
    files = [f for f in os.listdir(directory) if f.lower().endswith(file_extensions)]
    
    # Sort the files alphabetically (this assumes corresponding .png, .txt, .npz files have the same names)
    files.sort()

    # Counter for renaming
    counter = 1

    # Keep track of renamed files to avoid duplicates
    renamed_files = {}

    for file in files:
        # Get the base name and extension
        base_name, ext = os.path.splitext(file)

        # If this file has not been renamed yet, rename the image and its corresponding .txt and .npz files
        if base_name not in renamed_files:
            new_name = f"{counter:05d}"

            # Rename all matching files (.png, .txt, .npz)
            for extension in file_extensions:
                old_file = os.path.join(directory, f"{base_name}{extension}")
                if os.path.exists(old_file):
                    new_file = os.path.join(directory, f"{new_name}{extension}")

                    # Convert the .txt file to UTF-8 before renaming
                    if extension == '.txt':
                        convert_to_utf8(old_file)

                    os.rename(old_file, new_file)
                    print(f"Renamed {old_file} to {new_file}")

            # Increment the counter for the next set
            counter += 1
            renamed_files[base_name] = True


# Replace with the path to your directory
directory = r"C:\Users\umzg\Documents\Projektil\kohya_training_folder\7_art_by_bnha_short_description\7_art_by_bnha_short_description_processed_1024"
rename_files(directory)

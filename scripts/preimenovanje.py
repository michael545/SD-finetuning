import os
import shutil

source_folder = R"C:\Users\umzg\Documents\Projektil\Almanach\test" # mapa z originalnimi slikami
destination_folder = R"C:\Users\umzg\Documents\Projektil\clip_generated" # mapa za dodatne podmape za vsak pristop #mapa kamor se shranijo preimenovane slike

approaches = [
    "1_no_captions",
    "2_keyword_only_bnha",
    "3_art_by_bnha",
    "4_short_description_art_by_bnha",
    "7_art_by_bnha_short_description"
]

for approach in approaches:
    os.makedirs(os.path.join(destination_folder, approach), exist_ok=True)

images = [f for f in os.listdir(source_folder) if f.endswith(('png', 'jpg', 'jpeg'))]

def rename_and_move(image, approach_index, new_name):
    src = os.path.join(source_folder, image)
    dest = os.path.join(destination_folder, approaches[approach_index], new_name)
    shutil.copy(src, dest)  

for idx, image in enumerate(images, start=1):

    file_name, ext = os.path.splitext(image)

    rename_and_move(image, 0, f"{idx}{ext}")  # sekvencno brez captionov
    
    rename_and_move(image, 1, f"bnha_{idx}{ext}")  #  bnha_X

    rename_and_move(image, 2, f"art by bnha_{idx}{ext}")  # Rename as "art by bnha_X"

    rename_and_move(image, 3, f"{file_name}, art by bnha_{idx}{ext}")  # Short descriptive caption + "art by bnha"
    
    rename_and_move(image, 4, f"art by bnha_{idx}, {file_name}{ext}")  # "Art by bnha" + 

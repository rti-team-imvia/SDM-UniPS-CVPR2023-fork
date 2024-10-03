# Please refer to organize_data_to_SDM.md for more details about this script.

import os
import shutil

def select_equally_spaced_images(image_list, num_images_to_select=10):
    """
    Selects 'num_images_to_select' equally spaced images from the sorted image list.
    """
    total_images = len(image_list)
    if total_images <= num_images_to_select:
        return image_list  # If there are less or equal images, return all
    
    step = total_images // num_images_to_select
    selected_images = [image_list[i * step] for i in range(num_images_to_select)]
    
    return selected_images

def copy_and_rename_images(src_folder, dst_folder, selected_images, VERBOSE):
    """
    Copies and renames the selected images into the destination folder.
    """
    if not os.path.exists(dst_folder):
        os.makedirs(dst_folder)
    
    for i, image_file in enumerate(selected_images, 1):
        src_image_path = os.path.join(src_folder, image_file)
        dst_image_name = f"L ({i}).JPG"
        dst_image_path = os.path.join(dst_folder, dst_image_name)
        
        shutil.copy(src_image_path, dst_image_path)
        if VERBOSE:
            print(f"Copied and renamed: {src_image_path} -> {dst_image_path}")

def process_rti_folders(input_folder, VERBOSE):
    """
    Main function that processes all subfolders in the input folder, finds the images in the 'rti' folder,
    selects 10 equally spaced images, and copies/renames them into a new 'SDM_in' folder inside the 'rti' folder.
    """
    # Step 1: List all the folders in the input path
    for root_folder in os.listdir(input_folder):
        experiment_folder_path = os.path.join(input_folder, root_folder)
        
        if os.path.isdir(experiment_folder_path):
            # Step 2.1: Find the subfolder named "rti"
            for dirpath, dirnames, filenames in os.walk(experiment_folder_path):
                if "rti" in dirnames:
                    rti_folder_path = os.path.join(dirpath, "rti")
                    
                    # Step 2.2: Identify the images with extension JPG, and sort them in ascending order
                    jpg_images = sorted([f for f in os.listdir(rti_folder_path) if f.lower().endswith('.jpg')])
                    
                    if jpg_images:
                        # Step 2.3: Select 10 equally spaced images
                        selected_images = select_equally_spaced_images(jpg_images, num_images_to_select=10)
                        
                        # Step 2.4: Define the SDM_in.data folder path inside the rti folder
                        sdm_in_folder = os.path.join(rti_folder_path, "SDM_in.data")
                        
                        # Copy and rename the images into the SDM_in folder
                        copy_and_rename_images(rti_folder_path, sdm_in_folder, selected_images, VERBOSE)

if __name__ == "__main__":
    # Define the input folder (experiment folder path)
    input_folder = r"C:\Users\Deivid\Documents\rti-data\Palermo_3D\real acquisitions\head_cs"
    VERBOSE = True
    # Run the processing function
    process_rti_folders(input_folder, VERBOSE)

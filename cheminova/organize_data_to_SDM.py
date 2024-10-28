import shutil
from pathlib import Path
import argparse

def select_equally_spaced_images(image_list, num_images_to_select):
    """
    Selects 'num_images_to_select' equally spaced images from the sorted image list.
    If the number of images requested is greater than the available images, it returns all images.
    """
    total_images = len(image_list)
    if total_images <= num_images_to_select:
        return image_list  # If there are fewer or equal images, return all
    
    step = total_images // num_images_to_select
    selected_images = [image_list[i * step] for i in range(num_images_to_select)]
    
    return selected_images

def copy_and_rename_images(src_folder, dst_folder, selected_images, VERBOSE):
    """
    Copies and renames the selected images into the destination folder.
    """
    dst_folder.mkdir(parents=True, exist_ok=True)  # Create destination folder if it doesn't exist
    
    for i, image_file in enumerate(selected_images, 1):
        src_image_path = src_folder / image_file
        dst_image_name = f"L ({i}).JPG"
        dst_image_path = dst_folder / dst_image_name
        
        shutil.copy(src_image_path, dst_image_path)
        if VERBOSE:
            print(f"Copied and renamed: {src_image_path} -> {dst_image_path}")

def copy_mask_image(rti_folder_path, sdm_in_folder, VERBOSE):
    """
    Copies the 'mask.png' file from the rti folder to the SDM_in.data folder.
    """
    mask_image_path = rti_folder_path / "mask.png"
    if mask_image_path.exists():
        dst_mask_path = sdm_in_folder / "mask.png"
        shutil.copy(mask_image_path, dst_mask_path)
        if VERBOSE:
            print(f"Copied mask: {mask_image_path} -> {dst_mask_path}")
    else:
        if VERBOSE:
            print(f"WARNING: 'mask.png' not found in {rti_folder_path}.")

def process_rti_folders(input_folder, num_images, VERBOSE):
    """
    Main function that processes all subfolders in the input folder, finds the images in the 'rti' folder,
    selects the requested number of equally spaced images, and copies/renames them into a new 'SDM_in.data' folder inside the 'rti' folder.
    """
    # Step 1: List all the folders in the input path
    input_folder = Path(input_folder)  # Convert to a Path object for cross-platform compatibility
    for root_folder in input_folder.iterdir():
        if root_folder.is_dir():
            # Step 2.1: Find the subfolder named "rti"
            for rti_folder_path in root_folder.rglob("rti"):  # Search for 'rti' folder in subdirectories
                if rti_folder_path.is_dir():
                    # Step 2.2: Identify the images with extension JPG, and sort them in ascending order
                    jpg_images = sorted([f for f in rti_folder_path.iterdir() if f.suffix.lower() == '.jpg'])
                    total_images_found = len(jpg_images)

                    if jpg_images:
                        # If requested more images than available, show a warning
                        if total_images_found < num_images:
                            print(f"WARNING: Found only {total_images_found} images, but {num_images} were requested.")
                            selected_images = jpg_images  # Return all images if there are fewer than requested
                        else:
                            # Step 2.3: Select the requested number of equally spaced images
                            selected_images = select_equally_spaced_images(jpg_images, num_images)

                        # Step 2.4: Define the SDM_in folder path inside the rti folder
                        sdm_in_folder = rti_folder_path / "SDM_in.data"
                        
                        # Copy and rename the images into the SDM_in folder
                        copy_and_rename_images(rti_folder_path, sdm_in_folder, selected_images, VERBOSE)
                        
                        # Step 2.5: Copy the mask.png file if it exists
                        copy_mask_image(rti_folder_path, sdm_in_folder, VERBOSE)

if __name__ == "__main__":

    print('================================================================')
    print('                     Organize_data_to_SDM.py                    ')
    print('================================================================')   

    # Create an argument parser to accept command-line arguments
    parser = argparse.ArgumentParser(description="Process RTI folders and copy selected images into SDM_in.data folder.")
    parser.add_argument("--input_folder", type=str, help="Path to the input folder containing RTI data.")
    parser.add_argument("--num_images", type=int, default=10, help="Number of equally spaced images to select (default is 10).")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose mode to see more output.")

    # Parse the arguments
    args = parser.parse_args()

    """""""""
    SHOW PARAMETERS CHOSEN FOR THIS EXPERIMENT
    """""""""  
    for arg in vars(args):
        print(f'{arg} : {getattr(args, arg)}')
    print('================================================================')
    print('================================================================') 

    # Run the processing function with the provided input folder, number of images, and verbosity flag
    process_rti_folders(args.input_folder, args.num_images, args.verbose)

# python "cheminova/organize_data_to_SDM.py" --input_folder "C:/Users/Deivid/Documents/DiLiGenT-MV/DiLiGenT-MV/mvpmsData/bearPNG" --verbose --num_images 10
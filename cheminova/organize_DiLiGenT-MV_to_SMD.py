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
        dst_image_name = f"L ({i}).PNG"
        dst_image_path = dst_folder / dst_image_name
        
        shutil.copy(src_image_path, dst_image_path)
        if VERBOSE:
            print(f"Copied and renamed: {src_image_path} -> {dst_image_path}")

def process_viewpoint_folders(input_folder, num_images, VERBOSE):
    """
    Main function that processes all viewpoint subfolders in the input folder,
    selects the requested number of equally spaced images, and copies/renames them into a new 'SDM_in.data' folder inside each viewpoint folder.
    """
    # Step 1: List all the viewpoint folders in the input path
    input_folder = Path(input_folder)  # Convert to a Path object for cross-platform compatibility
    for viewpoint_folder in input_folder.iterdir():
        if viewpoint_folder.is_dir() and viewpoint_folder.name.startswith("view_"):
            # Step 2: Identify the images with extension PNG, and sort them in ascending order
            png_images = sorted([f for f in viewpoint_folder.iterdir() if f.suffix.lower() == '.png'])
            total_images_found = len(png_images)

            if png_images:
                # If requested more images than available, show a warning
                if total_images_found < num_images:
                    print(f"WARNING: Found only {total_images_found} images, but {num_images} were requested in {viewpoint_folder}.")
                    selected_images = png_images  # Return all images if there are fewer than requested
                else:
                    # Step 3: Select the requested number of equally spaced images
                    selected_images = select_equally_spaced_images(png_images, num_images)

                # Step 4: Define the SDM_in.data folder path inside each viewpoint folder
                sdm_in_folder = viewpoint_folder / "SDM_in.data"
                
                # Copy and rename the images into the SDM_in folder
                copy_and_rename_images(viewpoint_folder, sdm_in_folder, selected_images, VERBOSE)

if __name__ == "__main__":

    print('================================================================')
    print('             Oorganize_DiLiGenT-MV_to_SMD.py                    ')
    print('================================================================')   

    # Create an argument parser to accept command-line arguments
    parser = argparse.ArgumentParser(description="Process viewpoint folders and copy selected images into SDM_in.data folder.")
    parser.add_argument("--input_folder", type=str, help="Path to the input folder containing viewpoint folders.")
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
    process_viewpoint_folders(args.input_folder, args.num_images, args.verbose)

# python "cheminova/organize_DiLiGenT-MV_to_SMD.py" --input_folder "C:/Users/Deivid/Documents/DiLiGenT-MV/DiLiGenT-MV/mvpmsData/bearPNG" --verbose --num_images 10
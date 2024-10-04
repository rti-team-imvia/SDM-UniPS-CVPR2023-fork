import os
import subprocess
import shutil
import sys
import argparse
from pathlib import Path
from natsort import natsorted  # Import natsorted for natural sorting

def verify_sdm_in_folder(sdm_in_path):
    """
    Verify if the SDM_in.data folder has at least 10 images with the pattern 'L (x).JPG'.
    If more images are present, they will be logged. Raise an error if fewer than 10 are found.
    """
    # Generate the expected filenames for the first 10 images
    required_images = [f"L ({i}).JPG" for i in range(1, 11)]
    
    # Collect all images that match the naming pattern 'L (x).JPG' in the folder
    available_images = [f for f in os.listdir(sdm_in_path) if f.startswith("L (") and f.endswith(".JPG")]

    # Check if there are at least 10 images
    missing_images = [image for image in required_images if image not in available_images]

    if missing_images:
        raise FileNotFoundError(f"Missing required images: {', '.join(missing_images)}")

    # Log if there are additional images beyond the first 10
    extra_images = [image for image in available_images if image not in required_images]
    
    if extra_images:
        print(f"Additional images found: {', '.join(extra_images)}")

    print(f"Found {len(available_images)} valid images in {sdm_in_path}")

def run_sdm_unips_main(test_dir, session_name, checkpoint_path):
    """
    Run the main sdm_unips script using the same Python interpreter that runs this script.
    """
    subprocess.run([
        sys.executable, "sdm_unips/main.py",
        "--session_name", session_name,
        "--test_dir", test_dir,
        "--checkpoint", checkpoint_path,
        "--scalable"
    ], stdout=sys.stdout, stderr=sys.stderr, check=True)

def run_sdm_unips_relighting(datadir):
    """
    Run the relighting script using the same Python interpreter that runs this script.
    """
    subprocess.run([
        sys.executable, "sdm_unips/relighting.py",
        "--datadir", datadir,
        "--format", "avi"
    ], stdout=sys.stdout, stderr=sys.stderr, check=True)

def copy_output_to_sdm_out(results_folder, destination_folder):
    """
    Copy the output from the results folder to the SDM_out folder inside the 'rti' folder.
    """
    if not os.path.exists(destination_folder):
        os.makedirs(destination_folder)
    for file_name in os.listdir(results_folder):
        src_file_path = os.path.join(results_folder, file_name)
        dst_file_path = os.path.join(destination_folder, file_name)
        shutil.move(src_file_path, dst_file_path)

def clean_up_repository_output(session_output_folder):
    """
    Remove the session output folder from the repository.
    """
    shutil.rmtree(session_output_folder)

def process_acquisition_folders(input_folder, repository_path, checkpoint_path):
    """
    Process all acquisition folders and run the necessary scripts.
    """
    # Get a naturally sorted list of folders
    experiment_folders = natsorted(os.listdir(input_folder))

    for experiment_folder in experiment_folders:
        experiment_path = os.path.join(input_folder, experiment_folder)
        if os.path.isdir(experiment_path):
            # Find the SDM_in.data folder
            sdm_in_path = None
            for root, dirs, files in os.walk(experiment_path):
                for dir_name in dirs:
                    if dir_name == "SDM_in.data":
                        sdm_in_path = os.path.join(root, dir_name)
                        break
                if sdm_in_path:
                    break

            if not sdm_in_path:
                print(f"No 'SDM_in.data' folder found in {experiment_path}, skipping...")
                continue

            try:
                # Step 2: Verify the presence of the 10 images
                verify_sdm_in_folder(sdm_in_path)
                print(f"Verified images in {sdm_in_path}")

                # Step 3: Run sdm_unips/main.py
                session_name = experiment_folder
                test_dir = os.path.dirname(sdm_in_path)  # The parent folder of SDM_in.data
                run_sdm_unips_main(test_dir, session_name, checkpoint_path)
                print(f"Completed sdm_unips/main.py for {session_name}")

                # Step 5: Run sdm_unips/relighting.py
                results_data_dir = os.path.join(repository_path, session_name, "results", "SDM_in.data")
                run_sdm_unips_relighting(results_data_dir)
                print(f"Completed sdm_unips/relighting.py for {session_name}")

                # Step 6: Move the results to the existing SDM_out folder inside the 'rti' folder
                rti_folder = os.path.join(test_dir, "rti")
                sdm_out_path = os.path.join(rti_folder, "SDM_out")  # Use the existing rti/SDM_out path directly

                copy_output_to_sdm_out(results_data_dir, sdm_out_path)
                print(f"Moved output to {sdm_out_path}")

                # Step 8: Clean up the session output folder
                session_output_folder = os.path.join(repository_path, session_name)
                clean_up_repository_output(session_output_folder)
                print(f"Cleaned up {session_output_folder}")

            except Exception as e:
                print(f"Error processing {experiment_path}: {e}")

def main(input_folder):
    """
    Main function to handle argument parsing and trigger the processing.
    """

    # Ensure input path is a valid absolute path
    input_folder = Path(args.input_folder).resolve()

    # Assume repository_path is the current working directory
    repository_path = Path.cwd()

    # Checkpoint path is always inside the repository in the 'checkpoint' folder
    checkpoint_path = repository_path / "checkpoint"

    process_acquisition_folders(input_folder, str(repository_path), str(checkpoint_path))

if __name__ == "__main__":
    print('================================================================')
    print('                     Running run_sdm_multifolder.py              ')
    print('================================================================') 
    parser = argparse.ArgumentParser(description="Process SDM acquisition folders.")
    parser.add_argument("--input_folder", type=str, help="Path to the input folder containing acquisition data.")

    args = parser.parse_args()

    """""""""
    SHOW PARAMETERES CHOOSEN FOR THIS EXPERIMENT
    """""""""  
    for arg in vars(args):
        print(f'{arg} : {getattr(args, arg)}')
    print('================================================================')
    print('================================================================') 

    main(args.input_folder)

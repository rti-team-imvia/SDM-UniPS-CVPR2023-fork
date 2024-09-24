import os
import subprocess
import shutil
import sys

def verify_sdm_in_folder(sdm_in_path):
    """
    Verify if the SDM_in.data folder has the required 10 images. Raise an error if any are missing.
    """
    required_images = [f"L ({i}).JPG" for i in range(1, 11)]
    for image in required_images:
        image_path = os.path.join(sdm_in_path, image)
        if not os.path.exists(image_path):
            raise FileNotFoundError(f"Missing file: {image_path}")

def run_sdm_unips_main(test_dir, session_name, checkpoint_path, python_path):
    """
    Run the main sdm_unips script.
    """
    subprocess.run([
        python_path, "sdm_unips/main.py",
        "--session_name", session_name,
        "--test_dir", test_dir,
        "--checkpoint", checkpoint_path,
        "--scalable"
    ], stdout=sys.stdout, stderr=sys.stderr, check=True)

def run_sdm_unips_relighting(datadir, python_path):
    """
    Run the relighting script.
    """
    subprocess.run([
        python_path, "sdm_unips/relighting.py",
        "--datadir", datadir,
        "--format", "avi"
    ], stdout=sys.stdout, stderr=sys.stderr, check=True)

def copy_output_to_sdm_out(results_folder, destination_folder):
    """
    Copy the output from the results folder to the SDM_out folder at the same level as SDM_in.data.
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
    for experiment_folder in os.listdir(input_folder):
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
                run_sdm_unips_main(test_dir, session_name, checkpoint_path, os.path.join(repository_path, r'.venv\Scripts\python.exe'))
                print(f"Completed sdm_unips/main.py for {session_name}")

                # Step 5: Run sdm_unips/relighting.py
                results_data_dir = os.path.join(repository_path, session_name, "results", "SDM_in.data")
                run_sdm_unips_relighting(results_data_dir, os.path.join(repository_path, r'.venv\Scripts\python.exe'))
                print(f"Completed sdm_unips/relighting.py for {session_name}")

                # Step 6: Move the results to the SDM_out folder
                sdm_out_path = os.path.join(test_dir, "SDM_out")
                copy_output_to_sdm_out(results_data_dir, sdm_out_path)
                print(f"Moved output to {sdm_out_path}")

                # Step 8: Clean up the session output folder
                session_output_folder = os.path.join(repository_path, session_name)
                clean_up_repository_output(session_output_folder)
                print(f"Cleaned up {session_output_folder}")

            except Exception as e:
                print(f"Error processing {experiment_path}: {e}")

if __name__ == "__main__":
    print('================================================================')
    print('                     Running run_sdm_multifoder.py              ')
    print('================================================================') 

    # Define the paths
    input_folder = r"F:\dvd\Palermo_3D\real acquisitions\head_cs"
    repository_path = r"C:\Users\X-RTI\Documents\repos\SDM-UniPS-CVPR2023-fork" # Path to SDM-UniPS-CVPR2023-fork
    checkpoint_path = r"C:\Users\X-RTI\Documents\repos\SDM-UniPS-CVPR2023-fork\checkpoint"

    # Run the process
    process_acquisition_folders(input_folder, repository_path, checkpoint_path)

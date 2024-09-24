# run_sdm_multifolder

## Introduction:

This script was created to automate the process of running the `sdm_unips/main.py` and `sdm_unips/relighting.py` scripts across multiple RTI (Reflectance Transformation Imaging) acquisition. Each acquisition folder contains images that need to be processed using the SDM-UniPS-CVPR2023 repository to generate normal and reflectance maps, as well as a relit output video. 

The key reason for this script is to efficiently handle large numbers of acquisitions by:
- Iterating through all the acquisition folders.
- Verifying the required images are available in the `SDM_in.data` folder.
- Running the SDM-UniPS processes (`main.py` and `relighting.py`).
- Moving the outputs to their correct destination folders outside the repository.
- Cleaning up the temporary files in the repository to prevent clutter.

This automation significantly reduces manual work and ensures that the correct file structure and output names are maintained.

## How the Script Works:

1. **Input Folder**:
   - The script starts with a main input folder containing subfolders representing different RTI acquisitions.
   - Example: `C:\Users\Deivid\Documents\rti-data\Palermo_3D\real acquisitions\head_cs`

2. **Processing Each Acquisition Subfolder**:
   - For each acquisition folder (e.g., `2024_07_02_HEAD_CS_00`):
     - **Step 2.1**: The script searches recursively for a folder named `SDM_in.data`. This folder contains the images required for the SDM-UniPS process.
     - **Step 2.2**: It verifies that the `SDM_in.data` folder contains exactly 10 images named `L (1).JPG`, `L (2).JPG`, ..., `L (10).JPG`. If any are missing, an error is raised and logged.

3. **Running the SDM-UniPS Process**:
   - **Step 3**: Once the images are verified, the script runs the `sdm_unips/main.py` script with parameters:
     - `--session_name`: Set to the name of the current acquisition folder (e.g., `2024_07_02_HEAD_CS_00`).
     - `--test_dir`: Set to the folder containing `SDM_in.data`.
     - `--checkpoint`: The path to the model checkpoint.
   - This script processes the images and generates files like `baseColor.png`, `metallic.png`, etc., inside a `results` folder.

4. **Relighting**:
   - **Step 5**: After processing, the script runs `sdm_unips/relighting.py` to generate the final output video (`output.avi`) based on the processed images.

5. **Moving the Results**:
   - **Step 6**: The generated output from the `results` folder in the repository is moved into a new folder called `SDM_out` at the same level as `SDM_in.data` inside the original acquisition folder.

6. **Cleanup**:
   - **Step 8**: After the outputs are moved, the script deletes the session folder (e.g., `2024_07_02_HEAD_CS_00`) from the repository to keep the workspace clean.

7. **Loop for All Folders**:
   - The script repeats this process for all acquisition folders in the input directory.

## Requirements:

Same requirements for SDM-UNIPS-CVPR2023 repository.

## How to Use:

1. **Set the Paths**:
   - Update the variables in the script:
     - `input_folder`: Path to the main acquisition folder (e.g., `C:\Users\Deivid\Documents\rti-data\Palermo_3D\real acquisitions\head_cs`).
     - `repository_path`: Path to the SDM-UniPS repository (e.g., `C:\Users\Deivid\Documents\repos\SDM-UniPS-CVPR2023-fork`).
     - `checkpoint_path`: Path to the checkpoint model for SDM-UniPS.

2. **Run the Script**:
   - Execute the script. It will process each acquisition folder, run the required scripts, move the output files to the correct locations, and clean up temporary files.

3. **Output**:
   - For each acquisition, the script creates a folder `SDM_out` at the same level as the `SDM_in.data` folder. The generated outputs like `baseColor.png`, `normal.png`, `output.avi`, etc., will be placed in this folder.


# organize_data_to_SDM.py

This Python script processes folders containing RTI data, selects a specified number of equally spaced images from the `rti` folder, and copies them into a new folder named `SDM_in.data` within the `rti` folder. The images are renamed in a sequential format like `L (1).JPG`, `L (2).JPG`, etc.

## Functionality

1. **Input Folder**: The script takes a root folder path that contains multiple subfolders. Each subfolder is expected to have an `rti` folder inside which contains images with `.jpg` extension.
2. **Equally Spaced Images**: The script selects a number of images that are equally spaced from the sorted list of `.jpg` images.
3. **Custom Number of Images**: You can specify how many images to select using the `--num_images` argument. If fewer images are available than requested, all available images will be copied, and a warning will be shown.
4. **Renaming**: The selected images are renamed in the format `L (1).JPG`, `L (2).JPG`, etc., and are copied to a newly created folder `SDM_in.data` inside the `rti` folder.

## Arguments

- `--input_folder`: (Required) The path to the root folder containing the subfolders with RTI data.
- `--num_images`: (Optional) The number of equally spaced images to select from the `rti` folder. Default is 10.
- `--verbose`: (Optional) When included, prints additional information about the copying process.

## How to Use

You can run the script from the command line by providing the necessary arguments. Below is an example:

### Example Command:

```python
python .\cheminova\organize_data_to_SDM.py --input_folder "C:\Users\Deivid\Documents\rti-data\Palermo_3D\real acquisitions\head_cs" --verbose --num_images 10
```

## Parameters:
- `--input_folder`: Specifies the folder path that contains the subdirectories with rti folders.
- `--verbose`: Displays detailed output of the operations being performed.
- `--num_images 10`: Selects 10 equally spaced images from the rti folder.

## Sample Output:
If you run the script with the above command, you might see output like:

```bash
================================================================
                     Organize_data_to_SDM.py                    
================================================================
input_folder : C:\Users\Deivid\Documents\rti-data\Palermo_3D\real acquisitions\head_cs
num_images : 10
verbose : True
================================================================
================================================================
Copied and renamed: C:\Users\Deivid\Documents\rti-data\...\rti\image1.jpg -> C:\Users\Deivid\Documents\rti-data\...\rti\SDM_in.data\L (1).JPG
Copied and renamed: C:\Users\Deivid\Documents\rti-data\...\rti\image2.jpg -> C:\Users\Deivid\Documents\rti-data\...\rti\SDM_in.data\L (2).JPG
...
```

## Notes:
- If you request more images than are available in the rti folder, the script will automatically copy all available images and display a warning:

    ```bash
    WARNING: Found only 8 images, but 10 were requested.
    ```

- The SDM_in.data folder will be created within the rti folder for each subdirectory processed.
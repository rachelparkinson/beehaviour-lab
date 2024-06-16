import os
import glob
from functions.convert_vid import convert_h264_to_mp4

# Define the base path to the directory containing the subfolders

# Base directory containing many folders
main_directory = 'R:/Bee audio and video recordings/MC_data_Ellie'

# List all folders in the main directory
folders = [f for f in os.listdir(main_directory) if os.path.isdir(os.path.join(main_directory, f))]

# Loop through each folder in the main directory
for folder in folders:
    base_path = os.path.join(main_directory, folder)
    
    # List all subdirectories in the current folder
    subdirectories = [d for d in os.listdir(base_path) if os.path.isdir(os.path.join(base_path, d))]

    # Loop through each subdirectory
    for subdirectory in subdirectories:
        subfolder_path = os.path.join(base_path, subdirectory)

        # Find .h264 files in the current subfolder
        video_path = next(glob.iglob(f'{subfolder_path}/*[!_adj].h264'), None)

        # Check if an .mp4 file already exists
        mp4_files = glob.glob(f'{subfolder_path}/*.mp4')

        # If there is an .mp4 file, skip conversion
        if mp4_files:
            print(f"MP4 file already exists in {subfolder_path}, skipping conversion...")
            continue

        # Check if the essential files are found
        if not video_path:
            print(f"No .h264 files in {subfolder_path}, skipping...")
            continue

        # Call the conversion function
        convert_h264_to_mp4(video_path)
        
        print(f'{video_path} converted to mp4')
import os
import glob

# Define the base path to the directory containing the subfolders

# Base directory containing many folders
main_directory = 'R:/Bee audio and video recordings/Kieran_data/Video_adjusted'

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


# Find files in the current subfolder
        video_metadata_files = glob.glob(f'{subfolder_path}/*video_metadata.json')

        # Check if the essential file is found
        if not video_metadata_files:
            print(f"No video metadata files found in {subfolder_path}, skipping...")
            continue

        # Loop through each found file and rename it
        for video_metadata_file in video_metadata_files:
            new_file_name = video_metadata_file.replace('video_metadata.json', '_video_frames.json')
            os.rename(video_metadata_file, new_file_name)
            print(f"Renamed {video_metadata_file} to {new_file_name}")

print("Renaming process completed.")
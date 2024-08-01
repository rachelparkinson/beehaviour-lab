import os
import glob
import fnmatch
from functions.audio_ffmpeg import convert_wav_to_flac

# Define the base path to the directory containing the subfolders

# Base directory containing many folders
main_directory = '/Volumes/RFS/Bee audio and video recordings/MC_data_Ellie/Day_28'

# List all folders in the main directory
folders = [f for f in os.listdir(main_directory) if os.path.isdir(os.path.join(main_directory, f))]

# List all folders in the main directory that start with 'Day'
#folders = [f for f in os.listdir(main_directory) if os.path.isdir(os.path.join(main_directory, f)) and fnmatch.fnmatch(f, 'Day*')]

# Loop through each folder in the main directory
for folder in folders:
    base_path = os.path.join(main_directory, folder)
    
    # List all subdirectories in the current folder
    subdirectories = [d for d in os.listdir(base_path) if os.path.isdir(os.path.join(base_path, d))]

    # Loop through each subdirectory
    for subdirectory in subdirectories:
        subfolder_path = os.path.join(base_path, subdirectory)

        # Find .h264 files in the current subfolder
        audio_path = next(glob.iglob(f'{subfolder_path}/*.wav'), None)

        # Check if an .flac file already exists
        flac_files = glob.glob(f'{subfolder_path}/*.flac')

        # If there is an .mp4 file, skip conversion
        if flac_files:
            print(f"flac file already exists in {subfolder_path}, skipping conversion...")
            continue

        # Check if the essential files are found
        if not audio_path:
            print(f"No .wav files in {subfolder_path}, skipping...")
            continue

        # Call the conversion function
        convert_wav_to_flac(audio_path)
        
        print(f'{audio_path} converted to flac')
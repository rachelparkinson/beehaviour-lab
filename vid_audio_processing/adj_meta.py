import os
import glob
import json

# Define the base path to the directory containing the subfolders

# Base directory containing many folders
#main_directory = 'R:/RFS/Bee audio and video recordings/MC_data_Ellie'
main_directory = '/Volumes/RFS/Bee audio and video recordings/MC_data_Ellie/Day_29'

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
        metadata_files = glob.glob(f'{subfolder_path}/*metadata.json')

        # Check if the essential file is found
        if not metadata_files:
            print(f"No metadata files found in {subfolder_path}, skipping...")
            continue

        # Loop through each found file and edit it
        for metadata_file in metadata_files:
            # Read the JSON file
            with open(metadata_file, 'r') as file:
                data = json.load(file)
            
            # Modify the fields
            #if "background solution conc (M)" in data:
            #    data["background solution conc (M)"] = 2  # Change the value of "background solution conc (M)" to 2
            #else:
            #    data["background solution conc (M)"] = 2  # Add if it doesn't exist
            
            data["Day"] = 28  # Add a new entry "Day" with value 0
            data["background solution"] = "sucrose"
            data["background solution conc (M)"] = "2"
            data["pollen Y/N"] = "Y"
            data["group size"] = 5

            # Write the modified JSON back to the file
            with open(metadata_file, 'w') as file:
                json.dump(data, file, indent=4)
            
            print(f"Edited {metadata_file}")

print("Editing process completed.")

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

# Find files in the current subfolder
    metadata_files = glob.glob(f'{base_path}/*metadata.json')

    # Check if the essential file is found
    if not metadata_files:
        print(f"No video metadata files found in {base_path}, skipping...")
        continue

    # Loop through each found file and rename it
    for metadata_file in metadata_files:
        with open(metadata_file, 'r') as file:
            data = json.load(file)

        # Check if the key "ID" exists and change its value
        if 'ID' in data:
            data['ID'] = 'SFX_200'
            print(f"Updated ID in {metadata_file}")

        # Write the updated JSON back to the file
        with open(metadata_file, 'w') as file:
            json.dump(data, file, indent=4)

        print(f"Saved updated metadata file: {metadata_file}")        

print("Editing metadata process completed.")
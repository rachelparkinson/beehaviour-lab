import json
import os
import glob
from functions.media_info import get_frame_and_sample_rate, get_video_duration, get_frame_count
from functions.adjust_offset import adjust_audio_lag
from functions.video_speed import adjust_video_speed, change_video_fps

# Define the base path to the directory containing the subfolders

#TO DO:
#base_path = '/Volumes/RFS/Bee audio and video recordings/Kieran_data/240221-TMX5'
base_path = '/Volumes/RFS/Bee audio and video recordings/Kieran_data/240220-TMX1'
#base_path = '/Volumes/RFS/Bee audio and video recordings/Kieran_data/240228-SFX5'
#base_path = '/Volumes/RFS/Bee audio and video recordings/Kieran_data/240229-FLU5'


# List all subdirectories in the base path
subdirectories = [d for d in os.listdir(base_path) if os.path.isdir(os.path.join(base_path, d))]

# Loop through each subdirectory
for subdirectory in subdirectories:
    subfolder_path = os.path.join(base_path, subdirectory)

    # Find files in the current subfolder
    video_path = next(glob.iglob(f'{subfolder_path}/*[!_adj].mp4'), None)
    video_metadata = next(glob.iglob(f'{subfolder_path}/*video_metadata.json'), None)

    # Check if the essential files are found
    if not all([video_path, video_metadata]):
        print(f"Missing files in {subfolder_path}, skipping...")
        continue

    # Paths for adjusted video and output
    adj_video_path = video_path.replace('.mp4', '_adj_video.mp4')

    # video_frame_rate, audio_sample_rate = get_frame_and_sample_rate(video_path, audio_path)

    #if video_frame_rate:
        #print(f"Video Frame Rate: {video_frame_rate}")
    #else:
        #print("No video streams found in the file.")

    #if audio_sample_rate:
        #print(f"Audio Sample Rate: {audio_sample_rate}")
    #else:
        #print("No audio streams found in the file.")

    #frame_count_original = get_frame_count(video_path)
    #print(f"Frame Count original: {frame_count_original}")

    with open(video_metadata, 'r') as file:
        data = json.load(file)
        timestamps = data["timestamps"]  # Assuming 'timestamps' is the key containing the frame times
        frame_count = len(timestamps)
        print(f'There are {frame_count} frames in the "timestamps" variable.')

    # Example usage
    duration = get_video_duration(video_path)
    print(f"Duration: {duration} seconds")

    fps = str(frame_count/300)

    change_video_fps(video_path, adj_video_path, fps)
    
    print(f'{adj_video_path} saved')


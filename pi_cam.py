#Installations:
#sudo apt install -y python3-opencv
#sudo apt install -y opencv-data
#pip3 install tflite-runtime
#sudo apt install -y ffmpeg

from picamera2 import Picamera2, Preview
from picamera2.encoders import H264Encoder
import time
import json

def cam(framerate, resolution, video_file, duration, start_time):
    # Initialize camera
    picam2 = Picamera2()
    
    #Create video configuration
    video_config = picam2.create_video_configuration({
        "size": resolution,
        "framerate": framerate
    })
    
    #Configure the camera with the video config
    picam2.configure(video_config)
    
    #Initialize encoder
    encoder = H264Encoder(bitrate=10000000)

    # Calculate the end time
    end_time = start_time + duration
    
    # Create empty list to store timestamps
    timestamps = []
    
    # Start recording
    picam2.start_recording(encoder, video_file)
    
    while time.time() < end_time:
        current_time = time.time()
        timestamps.append(current_time)
        time.sleep(1)
    
    # stop recording
    picam2.stop_recording()
    
    # Save timestamps to a text file 
    with open(videop_file.replace('.h264', '_timestamps.txt'), 'w') as f:
        for timestamp in timestamps:
            f.write(f"{timestamp}\n")
    # or as a JSON file
    with open(video_file.replace('.h264', '_timestamps.json'), 'w') as f:
        json.dump(timestamps, f)
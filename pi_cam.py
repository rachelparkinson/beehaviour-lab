#Installations:
#sudo apt install -y python3-opencv
#sudo apt install -y opencv-data
#pip3 install tflite-runtime
#sudo apt install -y ffmpeg

from picamera2 import MappedArray, Picamera2, Preview
from picamera2.encoders import H264Encoder
import time
import os
import cv2
import json

def cam(picam2, framerate, resolution, video_file, duration, start_time):
    # Initialize camera
    #picam2 = Picamera2()
    
    #setup timestamp 
    hour = int(time.strftime('%H'))
    now = time.strftime("%y_%m_%d_%H_%M")
    colour = (255, 255, 255)
    origin = (0,30)
    font = cv2.FONT_HERSHEY_SIMPLEX
    scale = 1
    thickness = 2
    
    def apply_timestamp(request):
        current_time = time.time()
        milliseconds = (current_time - int(current_time)) * 1000
        timestamp = time.strftime("%Y-%m-%d %X") + f".{int(milliseconds):03d}"
        
        with MappedArray(request, "main") as m:
            cv2.putText(m.array, timestamp, origin, font, scale, colour, thickness)
    
    try:
        #Create video configuration
        #video_config = picam2.create_video_configuration({
        #    "size": resolution})
            #"framerate": framerate
            #})
        picam2.pre_callback = apply_timestamp
        picam2.video_configuration.size = resolution
        picam2.video_configuration.controls.FrameRate = framerate
    
        #Configure the camera with the video config
        #picam2.configure(video_config)
    
        #Initialize encoder
        encoder = H264Encoder(bitrate=10000000)

        # Calculate the end time
        #end_time = start_time + duration
    
        # Initialize frame counter and timestamps list
        #frame_count = 0
        #timestamps = []
    
        # Calculate time increment for each frame
        #frame_time_increment = 1.0 / framerate
    
        # Start recording
        #picam2.start_preview(Preview.QTGL)
        picam2.start_recording(encoder, video_file)
        
        time.sleep(duration)
    
        #while time.time() < end_time:
        #    current_time = start_time + (frame_count * frame_time_increment)
        #    timestamps.append(current_time)
        #    frame_count += 1
        #    time.sleep(frame_time_increment)
    
        # stop recording
        picam2.stop_recording()
        
        picam2.close()
    
        # Save frame info to JSON file with timestamps
        #output_data = {
        #    'frame_count': frame_count,
        #    'timestamps': timestamps
        #}
    
        #with open(video_file.replace('.h264', '_metadata.json'), 'w') as f:
        #    json.dump(output_data, f)
    
    except Exception as e:
        print(f"An error occurred: {e}")
    
    finally:
        # Close the camera
        picam2.close()
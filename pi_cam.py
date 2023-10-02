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
    
    try:
        #Create video configuration
        video_config = picam2.create_video_configuration({
            "size": resolution})
            #"framerate": framerate
            #})
    
        #Configure the camera with the video config
        picam2.configure(video_config)
    
        #Initialize encoder
        encoder = H264Encoder(bitrate=10000000)

        # Calculate the end time
        end_time = start_time + duration
    
        # Initialize frame counter and timestamps list
        frame_count = 0
        timestamps = []
    
        # Calculate time increment for each frame
        frame_time_increment = 1.0 / framerate
    
        # Start recording
        #picam2.start_preview(Preview.QTGL)
        picam2.start_recording(encoder, video_file)
    
        while time.time() < end_time:
            current_time = start_time + (frame_count * frame_time_increment)
            timestamps.append(current_time)
            frame_count += 1
            time.sleep(frame_time_increment)
    
        # stop recording
        picam2.stop_recording()
        
        picam2.close()
    
        # Save frame info to JSON file with timestamps
        output_data = {
            'frame_count': frame_count,
            'timestamps': timestamps
        }
    
        with open(video_file.replace('.h264', '_metadata.json'), 'w') as f:
            json.dump(output_data, f)
    
    except Exception as e:
        print(f"An error occurred: {e}")
    
    finally:
        # Close the camera
        picam2.close()
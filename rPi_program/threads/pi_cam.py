#Installations:
#sudo apt install -y python3-opencv
#sudo apt install -y opencv-data
#pip3 install tflite-runtime
#sudo apt install -y ffmpeg

from picamera2 import MappedArray, Picamera2, Preview
from picamera2.encoders import H264Encoder, Quality
from picamera2.outputs import FfmpegOutput
import time
import os
import cv2
import json
import subprocess

def record_video(picam2, framerate, resolution, video_file, Rec_time):
    
    #setup timestamp 
    hour = int(time.strftime('%H'))
    now = time.strftime("%y_%m_%d_%H_%M")
    colour = (255, 255, 255)
    origin = (0,30)
    font = cv2.FONT_HERSHEY_SIMPLEX
    scale = 1
    thickness = 2
    
    timestamps = []
    
    def apply_timestamp(request):
        current_time = time.time()
        milliseconds = (current_time - int(current_time)) * 1000
        timestamp = time.strftime("%Y-%m-%d %X") + f".{int(milliseconds):03d}"
        
        # Append timestamp to list
        timestamps.append(timestamp)
        
        with MappedArray(request, "main") as m:
            cv2.putText(m.array, timestamp, origin, font, scale, colour, thickness)
    
    try:
        #Create video configuration
        picam2.pre_callback = apply_timestamp
        picam2.video_configuration.size = resolution
        picam2.video_configuration.controls.FrameRate = framerate
        picam2.video_configuration.controls.Saturation = 0
        picam2.video_configuration.controls.ExposureTime = 10000
        picam2.video_configuration.controls.AnalogueGain = 1.5
    
        #Initialize encoder
        encoder = H264Encoder(bitrate=25000000)

        # Start recording
        picam2.start_recording(encoder, video_file)
        
        time.sleep(Rec_time)
    
        # stop recording
        picam2.stop_recording()
        
        picam2.close()
    
        # Save frame info to JSON file with timestamps
        output_data = {
            'timestamps': timestamps
            }
    
        with open(video_file.replace('.h264', 'frames_.json'), 'w') as f:
            json.dump(output_data, f)
    
    except Exception as e:
        print(f"An error occurred: {e}")
    
    finally:
        # Close the camera
        picam2.close()


def convert_h264_to_mp4(h264_video_file):
    mp4_file = h264_video_file.replace('.h264', '.mp4')
    ffmpeg_vid_command = [
        'ffmpeg',
        '-i', h264_video_file,  # Input file
        '-r', '45', # Framerate
        '-c:v', 'libx264',  # Video codec
        '-crf', '28',  # CRF value for compression
        '-preset', 'fast',  # Preset for compression-efficiency tradeoff
        '-f', 'mp4',  # Output file format
        mp4_file  # Output file
    ]
    
    try:
        subprocess.run(ffmpeg_vid_command, check=True)
        print(f"Converted {h264_video_file} to {mp4_file}")
        
        # Optionally, delete the original .h264 file
        os.remove(h264_video_file)
        
    except subprocess.CalledProcessError as e:
        print(f"Failed to convert {h264_video_file} to {mp4_file}: {e}")

    # ffmpeg -r 30 -i img%d.jpg -vcodec huffyuv output.avi
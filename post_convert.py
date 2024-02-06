import os
from pathlib import Path

from threads.USB_mic import convert_wav_to_flac
from threads.pi_cam import convert_h264_to_mp4

def find_and_convert_h264_files(start_directory):
    for root, dirs, files in os.walk(start_directory):
        for file in files:
            if file.endswith(".h264"):
                full_path = Path(root) / file
                convert_h264_to_mp4(full_path)
                
def find_and_convert_wav_files(start_directory):
    for root, dirs, files in os.walk(start_directory):
        for file in files:
            if file.endswith(".wav"):
                full_path = Path(root) / file
                convert_wav_to_flac(full_path)

# Specify the start directory here
start_directory = "/home/rPi1/WDSSD/240205"

print("finding and converting video files...")
find_and_convert_h264_files(start_directory)

print("finding and converting audio files...")
find_and_convert_wav_files(start_directory)

print("Compression & conversions complete.")
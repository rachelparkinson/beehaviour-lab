import os
import subprocess
import threading
import time

def record_audio(duration, audio_file):
    # Define command to record audio using arecord
    arecord_command = [
        'arecord',
        '-D', 'plughw:1,0', # use appropriate card,device numbers
        '-c', '1', 	#mono audio - use 2 for stereo
        '-r', '90000', #sample rate
        '-f', 'S16_LE',	# Audio format
        '-d', str(duration), #Recording duration in seconds
        audio_file	#output .wav file
    ]
    
    # Run the arecord command
    subprocess.run(arecord_command)

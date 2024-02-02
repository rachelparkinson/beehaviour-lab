import os
import subprocess
import threading
import time

def record_audio(Rec_time, audio_file, card, device):
    # Define command to record audio using arecord
    card_device = 'plughw:' + card + device
    
    arecord_command = [
        'arecord',
        '-D', card_device, # use appropriate card,device numbers
        '-c', '1', 	#mono audio - use 2 for stereo
        '-r', '90000', #sample rate
        '-f', 'S16_LE',	# Audio format
        '-d', str(Rec_time), #Recording duration in seconds
        audio_file	#output .wav file
    ]
    
    # Run the arecord command
    subprocess.run(arecord_command)

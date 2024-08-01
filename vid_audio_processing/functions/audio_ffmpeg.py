import os
import subprocess

def convert_wav_to_flac(wav_file):
    
    flac_file = os.path.splitext(wav_file)[0] + '.flac'
    
    ffmpeg_aud_command = [
        'ffmpeg',
        '-i', wav_file,  # Input file
        '-vn',  # No video
        '-ar', '90000',  # Sample rate
        '-ac', '1',  # Audio channels
        '-compression_level', '12',  # Highest compression level
        '-c:a', 'flac',  # Codec audio flac
        flac_file  # Output file
    ]
    
    # Run the ffmpeg command to convert wav to flac:
    #subprocess.run(ffmpeg_command)
    #return flac_file
    
    try:
        subprocess.run(ffmpeg_aud_command, check=True)
        print(f"Converted {wav_file} to {flac_file}")
        
        # Optionally, delete the original .wav file
        #os.remove(wav_file)
        
    except subprocess.CalledProcessError as e:
        print(f"Failed to convert {wav_file} to {flac_file}: {e}")
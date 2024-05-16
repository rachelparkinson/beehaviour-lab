import subprocess
import json

def get_media_info(file_path):
    cmd = ['ffprobe', '-v', 'quiet', '-print_format', 'json', '-show_streams', file_path]
    result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    return json.loads(result.stdout)

def get_frame_and_sample_rate(video_path, audio_path):
    video_info = get_media_info(video_path)
    audio_info = get_media_info(audio_path)
    
    video_frame_rate = None
    audio_sample_rate = None
    
    # Process video streams
    if video_info['streams']:
        for stream in video_info['streams']:
            if stream['codec_type'] == 'video':
                video_frame_rate = eval(stream['r_frame_rate'])
                break  # Break after finding the first video stream
    
    # Process audio streams
    if audio_info['streams']:
        for stream in audio_info['streams']:
            if stream['codec_type'] == 'audio':
                audio_sample_rate = int(stream['sample_rate'])
                break  # Break after finding the first audio stream
    
    return video_frame_rate, audio_sample_rate

def get_video_duration(video_path):
    cmd = [
        'ffprobe', '-v', 'error',
        '-show_entries', 'format=duration',
        '-of', 'default=noprint_wrappers=1:nokey=1',
        video_path
    ]
    result = subprocess.run(cmd, stdout=subprocess.PIPE, text=True)
    duration_seconds = float(result.stdout)
    return duration_seconds

import subprocess

def get_frame_count(video_path):
    cmd = [
        'ffprobe',
        '-v', 'error',  # Suppress errors
        '-select_streams', 'v:0',  # Select the first video stream
        '-count_frames',  # Count the frames
        '-show_entries', 'stream=nb_read_frames',  # Show the frame count
        '-of', 'default=nokey=1:noprint_wrappers=1',  # Output formatting options
        video_path  # The video file path
    ]
    result = subprocess.run(cmd, stdout=subprocess.PIPE, text=True)
    if result.stdout:
        return int(result.stdout.strip())
    else:
        return None


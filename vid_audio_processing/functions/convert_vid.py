import subprocess

def convert_h264_to_mp4(h264_video_file):
    mp4_file = h264_video_file.replace('.h264', '.mp4')
    ffmpeg_vid_command = [
        'ffmpeg',
        '-i', h264_video_file,  # Input file
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
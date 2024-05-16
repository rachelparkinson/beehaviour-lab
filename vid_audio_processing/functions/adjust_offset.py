import subprocess

def adjust_audio_lag(video_path, audio_path, output_path, audio_delay):
    cmd = [
        'ffmpeg', '-i', video_path, '-itsoffset', str(audio_delay), '-i', audio_path,
        '-c:v', 'copy', '-c:a', 'aac', '-strict', 'experimental', output_path
    ]
    subprocess.run(cmd)

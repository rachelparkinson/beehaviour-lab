import subprocess

def extract_segment(input_path, output_path, start_time, duration):
    cmd = ['ffmpeg', '-i', input_path, '-ss', str(start_time), '-t', str(duration), '-c', 'copy', output_path]
    subprocess.run(cmd)


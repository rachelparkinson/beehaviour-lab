import subprocess

def adjust_video_speed(video_path, output_path, speed_factor):
    cmd = [
        'ffmpeg', '-itsscale', str(1/speed_factor), '-i', video_path, output_path
    ]
    subprocess.run(cmd)

def change_video_fps(input_file, output_file, fps):
    """
    Change the video frame rate using mkvmerge.

    Args:
    input_file (str): Path to the input video file.
    output_file (str): Path to the output video file.
    fps (str): The new frame rate in "fps" or "numerator/denominator" format.
    """
    cmd = [
        'mkvmerge',
        '--default-duration',
        '0:{}fps'.format(fps),  # Applies the new FPS to the first (and typically only) video track
        '--fix-bitstream-timing-information', '0',
        input_file,
        '-o',
        output_file
    ]
    try:
        subprocess.run(cmd, check=True)
        print(f"Video frame rate changed successfully: {output_file}")
    except subprocess.CalledProcessError as e:
        print(f"Failed to change video frame rate: {e}")

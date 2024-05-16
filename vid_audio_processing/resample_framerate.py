from functions.media_info import get_frame_and_sample_rate, get_video_duration, get_frame_count
from functions.adjust_offset import adjust_audio_lag
from functions.video_speed import adjust_video_speed, change_video_fps

# Replace with your actual file paths
video_path = 'data/flying_video.mp4'
adj_video_path = 'data/adj_flying_vid.mp4'
audio_path = 'data/flying_audio.flac'
output_path = 'data/flying_combined.mp4'

video_frame_rate, audio_sample_rate = get_frame_and_sample_rate(video_path, audio_path)

if video_frame_rate:
    print(f"Video Frame Rate: {video_frame_rate}")
else:
    print("No video streams found in the file.")

if audio_sample_rate:
    print(f"Audio Sample Rate: {audio_sample_rate}")
else:
    print("No audio streams found in the file.")

frame_count_original = get_frame_count(video_path)
print(f"Frame Count original: {frame_count_original}")

# Example usage
duration = get_video_duration(video_path)
print(f"Duration: {duration} seconds")

fps = str(frame_count_original/300)

change_video_fps(video_path, adj_video_path, fps)

adj_video_frame_rate, audio_sample_rate = get_frame_and_sample_rate(adj_video_path, audio_path)

if adj_video_frame_rate:
    print(f"Compressed video Frame Rate: {adj_video_frame_rate}")
else:
    print("No video streams found in the file.")
    
#frame_count_original = get_frame_count(video_path)
frame_count_compressed = get_frame_count(adj_video_path)
print(f"Frame Count original: {frame_count_original}")
print(f"Frame Count compressed: {frame_count_compressed}")


from functions.adjust_offset import adjust_audio_lag

video_path = 'data/adj_flying_vid.mp4'
audio_path = 'data/flying_audio.flac'
output_path = 'data/flying_combined.mp4'

# Adjust 'audio_delay' to match the direction and magnitude of your lag (positive values delay the audio, negative values would delay the video)
adjust_audio_lag(video_path, audio_path, output_path, 0.01)
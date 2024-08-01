from functions.adjust_offset import adjust_audio_lag

video_path = '/Volumes/RFS/Bee audio and video recordings/MC_data_Ellie/Day_0/240205-SFX6/003/240205_3_rPi18_video_adj_video.mp4'
audio_path = '/Volumes/RFS/Bee audio and video recordings/MC_data_Ellie/Day_0/240205-SFX6/003/240205_3_rPi18_audio.flac'
output_path = '/Volumes/RFS/Bee audio and video recordings/MC_data_Ellie/Day_0/240205-SFX6/003/240205_rPi18_3_Aud_vid_combined.mp4'

# Adjust 'audio_delay' to match the direction and magnitude of your lag (positive values delay the audio, negative values would delay the video)
adjust_audio_lag(video_path, audio_path, output_path, 0.01)
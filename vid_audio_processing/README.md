# Video and audio file procesing

## Description
Programme for adjusting the frame duration on videos and aligning with audio recordings plus offset. 

## Files
resample_framerate.py --> recalculates the framerate of the video file knowing the number of frames (taken from the video_metadata file) and expected duration (5 minutes).

combine_vid_aud.py --> merge the separate audio and video files.

clip_media.py --> quick script to trim  files (i.e., extract segment from video)


## To do:
Need to check: is number of frames accurately represented in video_metadata.json files? If so, use this instead of querying as it takes forever.

Also: how accurate is the 0.01s time offset?

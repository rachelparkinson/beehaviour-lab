from functions.segment_cut import extract_segment

input_path = 'data/flying_combined.mp4'
output_path = 'data/bumblebee_seg_03.mp4'

# Extract a 1-minute segment starting from the desired time (e.g., 60 seconds into the file)
extract_segment(input_path, output_path, 70, 60)

import os
import glob
import subprocess
import argparse
from pathlib import Path

def create_30fps_version(input_video_path, output_30fps_path):
    """Create 30fps version from input video"""
    print(f"  Creating 30fps version from {os.path.basename(input_video_path)}...")
    cmd = [
        'ffmpeg', '-y',
        '-i', input_video_path,
        '-filter:v', 'fps=fps=30',
        '-c:v', 'libx264',
        '-preset', 'fast',
        '-crf', '23',
        '-c:a', 'copy',
        output_30fps_path
    ]
    
    subprocess.run(cmd, check=True, capture_output=True)
    print(f"  ✓ {os.path.basename(output_30fps_path)} created successfully")

def create_60s_clip(input_video_path, output_clip_path):
    """Create 60-second clip starting at 20 seconds"""
    print(f"  Creating 60-second clip starting at 20s...")
    clip_cmd = [
        'ffmpeg', '-y',
        '-i', input_video_path,
        '-ss', '20',  # Start at 20 seconds
        '-t', '60',   # Duration of 60 seconds
        '-c:v', 'libx264',
        '-preset', 'fast',
        '-crf', '23',
        '-c:a', 'copy',
        output_clip_path
    ]
    
    subprocess.run(clip_cmd, check=True, capture_output=True)
    print(f"  ✓ {os.path.basename(output_clip_path)} created successfully")

def resample_video_to_300s(input_video_path, output_300s_path):
    """Resample video to exactly 300 seconds"""
    # Get video duration to calculate the speed factor
    duration_cmd = [
        'ffprobe', '-v', 'error',
        '-show_entries', 'format=duration',
        '-of', 'default=noprint_wrappers=1:nokey=1',
        input_video_path
    ]
    
    result = subprocess.run(duration_cmd, capture_output=True, text=True, check=True)
    current_duration = float(result.stdout.strip())
    
    # Calculate speed factor to make video exactly 300 seconds
    speed_factor = current_duration / 300.0
    
    print(f"  Resampling video to exactly 300 seconds...")
    print(f"    Current duration: {current_duration:.2f}s")
    print(f"    Target duration: 300.00s")
    print(f"    Speed factor: {speed_factor:.4f}")
    
    cmd = [
        'ffmpeg', '-y',
        '-i', input_video_path,
        '-filter:v', f'setpts=PTS/{speed_factor}',
        '-c:v', 'libx264',
        '-preset', 'fast',
        '-crf', '23',
        '-c:a', 'copy',
        output_300s_path
    ]
    
    subprocess.run(cmd, check=True, capture_output=True)
    print(f"  ✓ {os.path.basename(output_300s_path)} created successfully")

def process_video_folder(folder_path, base_name, args):
    """Process a single video folder with the correct priority order"""
    print(f"\nProcessing folder: {os.path.relpath(folder_path, args.main_directory)}")
    
    # Define all possible input and output paths
    # Check both the base name and base name + _video for priority files
    original_video_path = os.path.join(folder_path, f"{base_name}_video.mp4")
    adj_video_path = os.path.join(folder_path, f"{base_name}_adj_video.mp4")
    resampled_video_path = os.path.join(folder_path, f"{base_name}_resampled.mp4")
    
    # Also check for files with _video suffix in the middle
    adj_video_path_with_video = os.path.join(folder_path, f"{base_name}_video_adj_video.mp4")
    resampled_video_path_with_video = os.path.join(folder_path, f"{base_name}_video_resampled.mp4")
    
    # Output files with _video_ prefix
    fps_30_path = os.path.join(folder_path, f"{base_name}_video_30fps.mp4")
    clip_60s_path = os.path.join(folder_path, f"{base_name}_video_60sclip.mp4")
    
    # Priority 1: Check for existing _video_adj_video.mp4 (already resampled to 300s)
    if os.path.exists(adj_video_path_with_video):
        print(f"  Found existing _video_adj_video.mp4 - using as input")
        input_video = adj_video_path_with_video
        skip_resampling = True
        
    # Priority 2: Check for existing _video_resampled.mp4 (already resampled to 300s)
    elif os.path.exists(resampled_video_path_with_video):
        print(f"  Found existing _video_resampled.mp4 - using as input")
        input_video = resampled_video_path_with_video
        skip_resampling = True
        
    # Priority 3: Use original _video.mp4 and resample to 300s FIRST, then reduce frame rate
    elif os.path.exists(original_video_path):
        print(f"  Using original _video.mp4 - will resample to 300s FIRST, then reduce frame rate")
        input_video = original_video_path
        skip_resampling = False
        
    else:
        print(f"  No suitable input video found - skipping folder")
        return False
    
    if skip_resampling:
        # Use existing resampled video - just create 30fps and clip
        print(f"  Skipping resampling step - using existing resampled video")
        
        # Create 30fps version from the resampled video
        create_30fps_version(input_video, fps_30_path)
        
        # Create 60s clip from the 30fps version
        create_60s_clip(fps_30_path, clip_60s_path)
        
    else:
        # Need to resample first, then create 30fps and clip
        print(f"  Processing original video: resample → 30fps → clip")
        
        # Step 1: Resample to exactly 300 seconds
        resample_video_to_300s(input_video, adj_video_path_with_video)
        
        # Step 2: Create 30fps version from the resampled 300s video
        create_30fps_version(adj_video_path_with_video, fps_30_path)
        
        # Step 3: Create 60s clip from the 30fps version
        create_60s_clip(fps_30_path, clip_60s_path)
    
    return True

def main():
    # Set up command line argument parsing
    parser = argparse.ArgumentParser(
        description='Process MP4 videos with correct priority order: _adj_video.mp4 > _resampled.mp4 > _video.mp4',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Processing Priority:
  1. Use existing *_adj_video.mp4 (already resampled to 300s)
  2. Use existing *_resampled.mp4 (already resampled to 300s)  
  3. Use *_video.mp4 and resample to 300s

Output files always created/overwritten:
  - *_30fps.mp4: 30fps version of input video
  - *_60sclip.mp4: 60-second clip starting at 20s

Examples:
  python resample_framerate.py                    # Process all folders
  python resample_framerate.py --overwrite        # Same behavior (always overwrites)
        """
    )
    
    parser.add_argument(
        '--overwrite', '-o',
        action='store_true',
        help='Overwrite existing processed files (default behavior)'
    )
    
    args = parser.parse_args()
    
    # Define the base path to the wild_bees directory
    args.main_directory = 'R:/Bee audio and video recordings/Group_data/wild_bees'
    
    # Alternative path if the above doesn't exist
    if not os.path.exists(args.main_directory):
        args.main_directory = 'E:/Group_data/wild_bees'
    
    if not os.path.exists(args.main_directory):
        print(f"Error: Directory {args.main_directory} not found!")
        print("Please update the main_directory path in the script.")
        return
    
    print(f"Processing videos in: {args.main_directory}")
    print("Processing Priority: _adj_video.mp4 > _resampled.mp4 > _video.mp4")
    print("Output files always created/overwritten")
    print("=" * 60)
    
    # Track processing statistics
    total_folders = 0
    successful_folders = 0
    failed_folders = 0
    
    # Walk through the directory structure: wild_bees → animal_subfolder → day_subfolder → replicate_subfolder
    for root, dirs, files in os.walk(args.main_directory):
        # Look for any video files in replicate_subfolders to get base names
        video_files = [f for f in files if f.endswith('.mp4')]
        
        if not video_files:
            continue
            
        print(f"\nDEBUG: Found {len(video_files)} video files in {os.path.relpath(root, args.main_directory)}:")
        for f in video_files:
            print(f"  - {f}")
            
        # Group files by base name (everything before the last underscore and extension)
        base_names = set()
        for video_file in video_files:
            # Extract base name by removing common suffixes
            base_name = video_file
            for suffix in ['_adj_video.mp4', '_resampled.mp4', '_30fps.mp4', '_60sclip.mp4', '_video.mp4']:
                if video_file.endswith(suffix):
                    base_name = video_file.replace(suffix, '')
                    break
            base_names.add(base_name)
            print(f"DEBUG: File '{video_file}' -> Base name: '{base_name}'")
        
        print(f"DEBUG: Unique base names found: {list(base_names)}")
        
        # Use the shortest base name (which is the core name without _video suffix)
        if base_names:
            # Sort by length and use the shortest (most likely the core name)
            base_name = min(base_names, key=len)
            print(f"DEBUG: Using shortest base name: '{base_name}'")
            
            total_folders += 1
            
            try:
                if process_video_folder(root, base_name, args):
                    successful_folders += 1
                else:
                    failed_folders += 1
            except Exception as e:
                print(f"  ✗ Error processing folder: {e}")
                failed_folders += 1
    
    # Print summary
    print("\n" + "=" * 60)
    print("PROCESSING SUMMARY")
    print("=" * 60)
    print(f"Total folders processed: {total_folders}")
    print(f"Successfully processed: {successful_folders}")
    print(f"Failed: {failed_folders}")
    
    if successful_folders > 0:
        print(f"\nOutput files created:")
        print(f"  - *_30fps.mp4: 30fps version of input video")
        print(f"  - *_60sclip.mp4: 60-second clips starting at 20 seconds")
        print(f"  - *_adj_video.mp4: Videos resampled to exactly 300 seconds (when needed)")
        print(f"\nNote: Original files are preserved. New files are created alongside them.")

if __name__ == "__main__":
    main()
import os
import json
import librosa
import matplotlib.pyplot as plt
import numpy as np
import soundfile as sf

main_directory = '/Volumes/RFS/Bee audio and video recordings/MC_data_Ellie'
file_list = 'FLU_MC_flac_paths.json'
saved_file_names_folder = os.path.join(main_directory, 'saved_file_paths')
audio_segments_folder = os.path.join(main_directory, 'audio_segments')
spectrograms_folder = os.path.join(main_directory, 'spectrograms')
error_log_file = os.path.join(main_directory, 'error_log.txt')

# Ensure output directories exist
os.makedirs(audio_segments_folder, exist_ok=True)
os.makedirs(spectrograms_folder, exist_ok=True)

def load_json_file():
    json_file_path = os.path.join(saved_file_names_folder, file_list)
    with open(json_file_path, 'r') as f:
        audio_file_list = json.load(f)
    return audio_file_list

def process_audio_file(file_path):
    try:
        y, sr = sf.read(file_path)

        # Extract and format the part of the path after 'MC_data_Ellie/'
        relative_path = file_path.split('MC_data_Ellie/')[1].replace('/', '_').replace('.flac', '')

        segments = [(10, 70), (70, 130), (160, 220), (220, 280)]
        
        for idx, (start, end) in enumerate(segments, 1):
            segment = y[start*sr:end*sr]
            segment_file_name = f"{relative_path}_{idx:02d}.wav"
            segment_file_path = os.path.join(audio_segments_folder, segment_file_name)
            
            sf.write(segment_file_path, segment, sr)  # Save the segment
            create_spectrogram(segment, sr, segment_file_name)
    except Exception as e:
        with open(error_log_file, 'a') as log:
            log.write(f"Error processing {file_path}: {e}\n")
        print(f"Error processing {file_path}: {e}")

def create_spectrogram(audio_data, sr, file_name):
    plt.figure(figsize=(10, 4))
    S = librosa.feature.melspectrogram(y=audio_data, sr=sr, n_mels=128)
    S_dB = librosa.power_to_db(S, ref=np.max)
    
    plt.pcolormesh(S_dB, shading='gouraud')
    plt.colorbar(format='%+2.0f dB')
    plt.title('Mel-frequency spectrogram')
    plt.tight_layout()
    
    spectrogram_file_name = f"{os.path.splitext(file_name)[0]}.png"
    spectrogram_file_path = os.path.join(spectrograms_folder, spectrogram_file_name)
    plt.savefig(spectrogram_file_path)
    plt.close()

def main():
    audio_file_list = load_json_file()
    for audio_file in audio_file_list:
        process_audio_file(audio_file)

if __name__ == "__main__":
    main()

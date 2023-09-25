import time
import board
import busio
import adafruit_ads1x15.ads1015 as ADS
from adafruit_ads1x15.analog_in import AnalogIn
import numpy as np
import wave
#import pyaudio <-- pip install this

def MEMs(data_queue, i2c, audio_file, duration, start_time):
    
    # Define the ADC object
    ads = ADS.ADS1015(i2c)
    chan = AnalogIn(ads, ADS.P0)

    # Parameters for audio recording
    sample_rate = 44100  # Sample rate (44100 Hz is standard for CD-quality audio)
    num_samples = int(sample_rate * duration)

    # Initialize audio buffer
    audio_data = np.zeros(num_samples, dtype=np.int16)

    # Calculate the expected end time for recording
    end_time = time.time() + duration

    # Record audio data from the microphone
    print("Recording...")
    for i in range(num_samples):
        audio_data[i] = chan.value

        # Check if the current time has exceeded the end time
        if time.time() >= end_time:
            break

        time.sleep(1 / sample_rate)

    print("Recording completed.")

    # Create an audio file and save the recorded data
    output_file = audio_file
    with wave.open(output_file, "wb") as wav_file:
        wav_file.setnchannels(1)  # Mono audio channel
        wav_file.setsampwidth(2)  # 2 bytes per sample (16-bit audio)
        wav_file.setframerate(sample_rate)
        wav_file.writeframes(audio_data.tobytes())

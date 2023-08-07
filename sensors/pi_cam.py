import picamera
import time

def cam(video_file, duration, resolution, framerate):


    with picamera.PiCamera() as camera:
        camera.resolution = resolution
        camera.framerate = framerate

        print("Recording video...")
        camera.start_recording(video_file, format='h264')
        camera.wait_recording(duration)
        camera.stop_recording()

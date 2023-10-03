# Kill camera processes - use this function when camera
# doesn't close properly on its own.
import os
import subprocess


def kill_camera_processes():
    try:
        # Run lsof command to check processes related to /dev/video0
        result = subprocess.check_output(['lsof', '/dev/video0']).decode('utf-8').strip()

        # Parse the output and extract the PIDs
        lines = result.split("\n")[1:]  # Skip the header line
        pids = [line.split()[1] for line in lines]  # Extract PID from each line

        if not pids:
            print("No camera processes found.")
            return

        # Kill the identified processes
        for pid in pids:
            subprocess.run(['kill', '-9', pid])
            print(f"Killed process with PID {pid}")

    except subprocess.CalledProcessError:
        print("No process currently accessing /dev/video0.")
    except Exception as e:
        print(f"Error: {e}")

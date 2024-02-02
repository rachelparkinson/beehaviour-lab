import subprocess
import re

def find_usb_mic():
    try:
        # Run the arecord -l command and capture its output
        result = subprocess.check_output(['arecord', '-l']).decode('utf-8')
        
        # Look for lines that describe a USB mic
        matches = re.finditer(r'card (\d+):.*?device (\d+): USB', result, re.MULTILINE)
        
        for match in matches:
            # Extract the card and device numbers
            card, device = match.groups()
            return int(card), int(device)
        
        raise ValueError("USB microphone not found.")
    except subprocess.CalledProcessError:
        raise RuntimeError("Error executing arecord command.")

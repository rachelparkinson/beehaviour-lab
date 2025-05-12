# Beehaviour Lab Raspberry Pi Program

## Description
Program to control rPi and components of Beehaviour Lab. 

## Installation
All files can be transferred to an rPi Model 4B to control: rPi NoIR camera (V2), Røde SmartLav+ lapel microphone, DHT22 temperature and humidity probe, LED lighting panels, time clapper (buzzer + LEDs), and OLED display screen.

## Usage
Update config.json with experiment-specific information, including recording segment length and number of replicates.

Run program from "main.py" file. 

## Requirements

Use a setup rPi to download all requirements, and then transfer to the other rPis using VNC. 

# 1. on the Internet-connected rPi:

```
#!/bin/bash

# Create directories for packages
mkdir -p rpi_packages/apt
mkdir -p rpi_packages/pip

# Download apt packages and dependencies
cd rpi_packages/apt
apt-get download \
    python3-opencv \
    opencv-data \
    ffmpeg \
    $(apt-cache depends python3-opencv opencv-data ffmpeg | grep -E 'Depends|Recommends|Suggests' | cut -d: -f2 | tr -d '<>' | sed '/^$/d')

# Download pip packages (will automatically get ARM-compatible versions from piwheels)
cd ../pip
pip3 download \
    opencv-python \
    picamera2 \
    tflite-runtime

# Create tar archive
cd ../..
tar -czvf rpi_packages.tar.gz rpi_packages/
```

# 2. on the other rPis:

```
#!/bin/bash

# Extract the archive
tar -xzvf rpi_packages.tar.gz

# Install apt packages
cd rpi_packages/apt
sudo dpkg -i *.deb

# Handle any dependency issues
sudo apt --fix-broken install

# Install pip packages
cd ../pip
pip3 install --no-index --find-links . *.whl
```


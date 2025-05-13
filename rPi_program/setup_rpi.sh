{\rtf1\ansi\ansicpg1252\cocoartf2822
\cocoatextscaling0\cocoaplatform0{\fonttbl\f0\fswiss\fcharset0 Helvetica;}
{\colortbl;\red255\green255\blue255;}
{\*\expandedcolortbl;;}
\paperw11900\paperh16840\margl1440\margr1440\vieww11520\viewh8400\viewkind0
\pard\tx720\tx1440\tx2160\tx2880\tx3600\tx4320\tx5040\tx5760\tx6480\tx7200\tx7920\tx8640\pardirnatural\partightenfactor0

\f0\fs24 \cf0 #!/bin/bash\
\
set -e\
\
# ---- SYSTEM UPDATE & CORE APT PACKAGES ----\
echo "Updating and installing apt packages..."\
sudo apt-get update\
sudo apt-get install -y \\\
    gparted \\\
    python3-opencv \\\
    opencv-data \\\
    ffmpeg \\\
    alsa-utils \\\
    pulseaudio \\\
    i2c-tools \\\
    python3-smbus \\\
    python3-numpy \\\
    tigervnc-standalone-server \\\
    tigervnc-common \\\
    nano \\\
    raspi-config\
\
# ---- FIX NUMPY ISSUE ----\
echo "Ensuring numpy comes from apt..."\
pip3 uninstall -y numpy || true\
sudo apt-get install -y python3-numpy\
\
# ---- PIP PACKAGE INSTALL ----\
echo "Installing pip packages..."\
pip3 install --upgrade pip\
pip3 install \\\
    adafruit-circuitpython-dht \\\
    adafruit-circuitpython-ssd1306 \\\
    adafruit-blinka \\\
    tflite-runtime \\\
    opencv-python \\\
    picamera2 \\\
    RPi.GPIO \\\
    board \\\
    busio\
\
# ---- BASHRC PATH FIX ----\
echo "Ensuring ~/.local/bin is in PATH..."\
grep -qxF 'export PATH="$HOME/.local/bin:$PATH"' ~/.bashrc || echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.bashrc\
source ~/.bashrc\
\
# ---- ENABLE VNC + SSH + AUTOLOGIN + DISPLAY ----\
echo "Configuring system settings via raspi-config..."\
\
# Enable VNC\
sudo raspi-config nonint do_vnc 0\
\
# Enable SSH\
sudo raspi-config nonint do_ssh 0\
\
# Enable desktop autologin for 'pi' user\
sudo raspi-config nonint do_boot_behaviour B4\
\
# Set resolution to 1280x720\
sudo raspi-config nonint do_resolution 85 16  # mode 85 is 1280x720 60Hz\
\
# ---- ENABLE I2C IN CONFIG.TXT ----\
echo "Enabling I2C in /boot/config.txt..."\
sudo sed -i 's/^#dtparam=i2c_arm=on/dtparam=i2c_arm=on/' /boot/config.txt\
\
# ---- VNC PASSWORD ----\
echo "Setting VNC password for user $USER..."\
vncpasswd\
\
echo "All setup steps complete. Reboot recommended."\
}
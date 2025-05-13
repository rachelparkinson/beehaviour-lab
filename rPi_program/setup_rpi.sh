#!/bin/bash

set -e

# ---- SYSTEM UPDATE & CORE APT PACKAGES ----
echo "Updating and installing apt packages..."
sudo apt-get update
sudo apt-get install -y \
    gparted \
    python3-opencv \
    opencv-data \
    ffmpeg \
    alsa-utils \
    pulseaudio \
    i2c-tools \
    python3-smbus \
    python3-numpy \
    nano \
    raspi-config \
    libcap-dev

# ---- REMOVE TIGERVNC IF INSTALLED ----
echo "Removing TigerVNC to avoid conflicts with RealVNC..."
sudo apt-get remove -y tigervnc-standalone-server tigervnc-common || true


# ---- CREATE VENV ----
echo "Creating virtual environment..."
python3 -m venv ~/venv
source ~/venv/bin/activate

echo "Installing pip packages into virtualenv..."
pip install --upgrade pip
pip install \
    adafruit-circuitpython-dht \
    adafruit-circuitpython-ssd1306 \
    adafruit-blinka \
    tflite-runtime \
    opencv-python \
    picamera2 \
    RPi.GPIO \
    board

# ---- BASHRC PATH FIX (OPTIONAL) ----
echo "Ensuring ~/.local/bin is in PATH..."
grep -qxF 'export PATH="$HOME/.local/bin:$PATH"' ~/.bashrc || echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.bashrc

# ---- ENABLE VNC + SSH + AUTOLOGIN + DISPLAY ----
echo "Configuring system settings via raspi-config..."

# Enable built-in RealVNC and SSH
sudo raspi-config nonint do_vnc 0
sudo raspi-config nonint do_ssh 0

# Enable desktop autologin for 'pi' user
sudo raspi-config nonint do_boot_behaviour B4

# Set resolution to 1280x720 (85 16)
sudo raspi-config nonint do_resolution 85 16

# ---- ENABLE I2C IN CONFIG.TXT ----
echo "Enabling I2C in /boot/config.txt..."
sudo sed -i 's/^#dtparam=i2c_arm=on/dtparam=i2c_arm=on/' /boot/config.txt

# ---- MICROPHONE SETUP ----
echo "Disabling onboard audio to prioritize USB microphone..."
sudo sed -i 's/^dtparam=audio=on/dtparam=audio=off/' /boot/config.txt

# ---- WIFI SETUP ----
echo "Setting up Wi-Fi networks with priorities..."

sudo tee /etc/wpa_supplicant/wpa_supplicant.conf > /dev/null <<EOF
ctrl_interface=DIR=/var/run/wpa_supplicant GROUP=netdev
update_config=1
country=GB

network={
    ssid="Rachel's iPhone (6)"
    psk="Hello239"
    priority=1
}

network={
    ssid="ETHOSCOPE_WIFI"
    psk="ETHOSCOPE_1234"
    priority=2
}
EOF

sudo chmod 600 /etc/wpa_supplicant/wpa_supplicant.conf


# ---- FINAL REBOOT PROMPT ----
echo "All setup steps complete. RealVNC will start on boot using system login."
read -p "Reboot now? [y/N]: " confirm && [[ $confirm == [yY] ]] && sudo reboot

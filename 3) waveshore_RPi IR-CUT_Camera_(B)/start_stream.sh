#!/bin/bash

# Uruchomienie VLC w tle
echo "Uruchamiam VLC..."

# Network caching ustawione na 2s aby zminimalizowac przycinanie
vlc udp://@:5000 --demux=h264 --network-caching=2000 &

# Krótkie opóźnienie, aby dać VLC czas na uruchomienie
sleep 2

# Połączenie z Raspberry Pi i uruchomienie libcamera-vid
echo "Łączenie z Raspberry Pi..."
ssh pi@192.168.1.101 "libcamera-vid --level 4.2 --framerate 30 --width 1280 --height 720 --inline --denoise cdn_off -n -t 0 -o udp://192.168.1.100:5000"

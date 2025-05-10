# 🌐 Waveshare PoE HAT B – Autostart jako Usługa systemd

Ten projekt uruchamia skrypt Python obsługujący wyświetlacz OLED Waveshare PoE HAT B jako usługę systemową w systemie Linux (np. Raspberry Pi OS).

## 📋 Wymagania

- Python 3
- Raspberry Pi OS lub inny system oparty na Debianie
- Moduły: `RPi.GPIO`, `smbus`

## ⚙️ Instalacja

### 1. Zainstaluj zależności

```bash
sudo apt-get update
sudo apt-get install -y python3-pip python3-smbus
sudo pip3 install RPi.GPIO
```

### Select Interacting Options ->I2C ->yes to start the I2C kernel driver

```bash
sudo raspi-config
```


### 2. Sklonuj repozytorium

```bash
mkdir -p ~/Scripts
cd ~/Scripts
git clone https://github.com/KarolDawidG/py-scripts-collection.git
```

### 3. Przenieś projekt do prostszej ścieżki

```bash
mkdir -p ~/PoE_HAT_B
mv ~/Scripts/py-scripts-collection/1\)\ waveshare_POE_HAT_B/* ~/PoE_HAT_B/
```

### 4. Utwórz plik usługi systemd

```bash
sudo nano /etc/systemd/system/my_script.service
```

Wklej do pliku:

```ini
[Unit]
Description=My Python Script

[Service]
ExecStart=/usr/bin/python3 /home/dawid/PoE_HAT_B/main.py
WorkingDirectory=/home/dawid/PoE_HAT_B
StandardOutput=inherit
StandardError=inherit
Restart=always
User=dawid

[Install]
WantedBy=multi-user.target
```

### 5. Włącz i uruchom usługę

```bash
sudo systemctl daemon-reexec
sudo systemctl enable my_script.service
sudo systemctl start my_script.service
```

### 6. Sprawdź status

```bash
systemctl status my_script.service
```

## 🛠️ Debugowanie

Aby wyświetlić logi działania skryptu:

```bash
journalctl -u my_script.service -f
```

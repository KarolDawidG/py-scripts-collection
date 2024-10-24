First, create new file in this location:

sudo nano /etc/systemd/system/my_script.service

you need to type:

[Unit]
Description=My Python Script

[Service]
ExecStart=/usr/bin/python /home/dawid/PoE_HAT_B/main.py
WorkingDirectory=/home/dawid/PoE_HAT_B
StandardOutput=inherit
StandardError=inherit
Restart=always
User=dawid

[Install]
WantedBy=multi-user.target


and in this line:
ExecStart=/usr/bin/python /home/dawid/PoE_HAT_B/main.py

you should provide path to your main.py file


After that execute command:
sudo systemctl enable my_script.service
sudo systemctl start my_script.service
sudo systemctl status my_script.service


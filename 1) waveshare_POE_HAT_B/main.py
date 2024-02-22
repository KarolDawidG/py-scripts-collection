import time
import logging
from POE_HAT_B import POE_HAT_B  # Importujesz klas? POE_HAT_B bezpo?rednio
from WiadomoscNaEkranie import WiadomoscNaEkranie

# Konfiguracja logowania
logging.basicConfig(level=logging.INFO)

# Tworzenie instancji klas
POE = POE_HAT_B()
wiadomosc_na_ekranie = WiadomoscNaEkranie()

# Wy?wietlanie wiadomo?ci powitalnej
# POE.Display_Welcome_Message()
wiadomosc_na_ekranie.wyswietl_wiadomosc("testowa")

try:
    while True:
        POE.POE_HAT_Display(43)  # U?ywanie funkcji z klasy POE_HAT_B
        time.sleep(1)
except KeyboardInterrupt:
    print("ctrl + c:")
    POE.FAN_OFF()

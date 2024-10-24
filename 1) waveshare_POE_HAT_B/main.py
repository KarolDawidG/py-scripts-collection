import time
import logging
from POE_HAT_B import POE_HAT_B
from WiadomoscNaEkranie import WiadomoscNaEkranie

logging.basicConfig(level=logging.INFO)

POE = POE_HAT_B()
wiadomosc_na_ekranie = WiadomoscNaEkranie()

wiadomosc_na_ekranie.wyswietl_wiadomosc("testowa")

try:
    while True:
        POE.POE_HAT_Display(43)
        time.sleep(1)
except KeyboardInterrupt:
    print("ctrl + c:")
    POE.FAN_OFF()

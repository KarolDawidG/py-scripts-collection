from SSD1306 import SSD1306
from PIL import Image, ImageDraw, ImageFont

class WiadomoscNaEkranie:
    def __init__(self):
        self.display = SSD1306()
        self.display.Init()
        self.font = ImageFont.load_default()

    def wyswietl_wiadomosc(self, wiadomosc):
        image = Image.new('1', (self.display.width, self.display.height), "WHITE")
        draw = ImageDraw.Draw(image)
        draw.text((10, 15), wiadomosc, font=self.font, fill=0)
        self.display.ShowImage(self.display.getbuffer(image))

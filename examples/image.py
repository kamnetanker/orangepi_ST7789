#!/usr/bin/env python3
import sys

from PIL import Image
from st7789 import ST7789

SPI_PORT = 0
SPI_CS = 0
SPI_DC = 27    # PA0
SPI_RES = 17   # PA1
BACKLIGHT = 22 # PA3

try:
    image_file = sys.argv[1]
except IndexError:
    image_file = "./examples/cat.jpg"

try:
    display_type = sys.argv[2]
except IndexError:
    display_type = "dhmini"

print("""
image.py - Display an image on the LCD.

If you're using Breakout Garden, plug the 1.3" LCD (SPI)
breakout into the front slot.

""")

print("""Usage: {} <image_file> <display_type>

Where <display_type> is one of:
  * square - 240x240 1.3" Square LCD
  * round  - 240x240 1.3" Round LCD (applies an offset)
  * rect   - 240x135 1.14" Rectangular LCD (applies an offset)
  * dhmini - 320x240 2.0" Display HAT Mini 
""".format(sys.argv[0]))

# Create ST7789 LCD display class.

if display_type in ("square", "rect", "round"):
    disp = ST7789(
        height=135 if display_type == "rect" else 240,
        rotation=0 if display_type == "rect" else 90,
        port=0,
        cs=ST7789.BG_SPI_CS_FRONT,  # BG_SPI_CS_BACK or BG_SPI_CS_FRONT
        dc=9,
        backlight=19,               # 18 for back BG slot, 19 for front BG slot.
        spi_speed_hz=80 * 1000 * 1000,
        offset_left=0 if display_type == "square" else 40,
        offset_top=53 if display_type == "rect" else 0
    )

elif display_type == "dhmini":
    disp = ST7789(
        height=240,
        width=320,
        rotation=0,
        port=SPI_PORT,
        cs=SPI_CS,
        dc=SPI_DC,
        rst=SPI_RES,
        backlight=BACKLIGHT,
        spi_speed_hz=60 * 1000 * 1000,
        offset_left=0,
        offset_top=0
   )

else:
    print ("Invalid display type!")

WIDTH = disp.width
HEIGHT = disp.height

# Initialize display.
disp.begin()

# Load an image.
print('Loading image: {}...'.format(image_file))
image = Image.open(image_file)

# Resize the image
image = image.resize((WIDTH, HEIGHT))

# Draw the image on the display hardware.
print('Drawing image')

disp.display(image)

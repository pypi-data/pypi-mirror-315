# SPDX-FileCopyrightText: 2024 Tim Cocks for Adafruit Industries
# SPDX-FileCopyrightText: 2024 Jose D. Montoya
#
# SPDX-License-Identifier: MIT

import time
import board
from adafruit_display_text.bitmap_label import Label
from terminalio import FONT
from displayio import Group
import adafruit_bmp280

# Simple demo of the BMP280 barometric pressure sensor.
# create a main_group to hold anything we want to show on the display.
main_group = Group()
# Initialize I2C bus and sensor.
i2c = board.I2C()  # uses board.SCL and board.SDA
bmp280 = adafruit_bmp280.Adafruit_BMP280_I2C(i2c)

# change this to match the location's pressure (hPa) at sea level
bmp280.sea_level_pressure = 1013.25

# Create two Labels to show the readings. If you have a very small
# display you may need to change to scale=1.
tempandpress_output_label = Label(FONT, text="", scale=2)
altitude_output_label = Label(FONT, text="", scale=2)

# place the labels in the middle of the screen with anchored positioning
tempandpress_output_label.anchor_point = (0, 0)
tempandpress_output_label.anchored_position = (
    4,
    board.DISPLAY.height // 2 - 40,
)
altitude_output_label.anchor_point = (0, 0)
altitude_output_label.anchored_position = (4, board.DISPLAY.height // 2 + 20)


# add the label to the main_group
main_group.append(tempandpress_output_label)
main_group.append(altitude_output_label)

# set the main_group as the root_group of the built-in DISPLAY
board.DISPLAY.root_group = main_group

# begin main loop
while True:
    # Update the label.text property to change the text on the display
    tempandpress_output_label.text = (
        f"Temperature:{bmp280.temperature:0.1f} C \nPressure:{bmp280.pressure:0.1f} hPa"
    )
    altitude_output_label.text = f"Altitude:{bmp280.altitude:0.2f} mts"
    # wait for a bit
    time.sleep(2.0)

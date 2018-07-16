#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pygame
import subprocess
import signal
import sys
from time import sleep
import Adafruit_MPR121.MPR121 as MPR121

print("""
==============================
  Fruit Piano? FRUIT PIANO!
==============================
""")

shutdown_command = '/usr/bin/sudo /sbin/shutdown -h now'

# Create MPR121 instance.
cap = MPR121.MPR121()

# Initialize communication with MPR121 using default I2C bus of device, and
# default I2C address (0x5A).  On BeagleBone Black will default to I2C bus 0.
if not cap.begin():
    print('Error initializing MPR121.  Check your wiring!')
    sys.exit(1)

# handle ctrl+c gracefully
def signal_handler(signal, frame):
  sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)

# LET THERE BE MUSIC!
pygame.init()
pygame.mixer.pre_init(44100, -16, 12, 512)
pygame.mixer.init()
volume = 1
pygame.mixer.music.set_volume(volume)
source_folder = "synths"
channels = ["mario", "piano"]
num_channels = len(channels) - 1
current_channel = 0


# LET DECISIONS HAPPEN!
def change_sounds():
    global current_channel
    next_channel = current_channel + 1

    if(next_channel > num_channels):
        next_channel = 0

    current_channel = next_channel
    print("channel: " + str(current_channel) + " / " + channels[current_channel])

last_touched = cap.touched()

try:

    while True:
        current_touched = cap.touched()
        # Check each pin's last and current state to see if it was pressed or released.
        for i in range(12):
            # Each pin is represented by a bit in the touched value.  A value of 1
            # means the pin is being touched, and 0 means it is not being touched.
            pin_bit = 1 << i
            # Check if the sound switching key has been pressed, if so, increment the offset by 12.
            # First check if transitioned from not touched to touched.

            if current_touched & pin_bit and not last_touched & pin_bit:

              source_folder = channels[current_channel]
              song = "/home/pi/fruitplayer/sfx/" + source_folder + "/" + str(i) + ".wav"
              sound = pygame.mixer.Sound(song)
              print('{0} touched!'.format(i))

              if(i == 11):
                  change_sounds()
                  sleep(0.5)

              if(i == 10):
                  sound.play(0)
                  print("Sample: " + str(i))
                  sleep(5)
                  subprocess.Popen(shutdown_command.split())

              else:
                  sound.play(0)
                  print("Sample: " + str(i))

            if not current_touched & pin_bit and last_touched & pin_bit:
                print('{0} released!'.format(i))

        last_touched = current_touched
        sleep(0.01)

except KeyboardInterrupt:
    # kill the piano if the user hits ctrl+c
    print("""
==============================
FRUIT PIANO! OUT!
==============================
    """)

#!/usr/bin/python
# Copyright (c) 2014 Adafruit Industries
# Author: Tony DiCola
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
import sys
import time
import subprocess
import pygame

import Adafruit_MPR121.MPR121 as MPR121

# Thanks to Scott Garner & BeetBox!
# https://github.com/scottgarner/BeetBox/

print 'Adafruit MPR121 Capacitive Touch Audio Player Test'

# Create MPR121 instance.
cap = MPR121.MPR121()

# Initialize communication with MPR121 using default I2C bus of device, and
# default I2C address (0x5A).  On BeagleBone Black will default to I2C bus 0.
if not cap.begin():
    print('Error initializing MPR121.  Check your wiring!')
    sys.exit(1)

# Alternatively, specify a custom I2C address such as 0x5B (ADDR tied to 3.3V),
# 0x5C (ADDR tied to SDA), or 0x5D (ADDR tied to SCL).
#cap.begin(address=0x5B)

# Also you can specify an optional I2C bus with the bus keyword parameter.
#cap.begin(busnum=1)

pygame.mixer.pre_init(44100, -16, 12, 512)
pygame.init()

# Define mapping of capacitive touch pin presses to sound files
# tons more sounds are available but because they have changed to .wav in /opt/sonic-pi/etc/samples/ some will not work
# more .wav files are found in /usr/share/scratch/Media/Sounds/ that work fine this example uses Aniamal sounds.

SOUND_MAPPING= {
  0: '/opt/sonic-pi/etc/samples/ambi_piano.wav',
  1: '/opt/sonic-pi/etc/samples/elec_hollow_kick.wav',
  2: '/opt/sonic-pi/etc/samples/ambi_soft_buzz.wav',
  3: '/opt/sonic-pi/etc/samples/bass_dnb_f.wav',
  4: '/opt/sonic-pi/etc/samples/bass_hit_c.wav',
  5: '/opt/sonic-pi/etc/samples/elec_plip.wav',
  6: '/opt/sonic-pi/etc/samples/bass_trance_c.wav',
  7: '/opt/sonic-pi/etc/samples/vinyl_backspin.wav',
  8: '/opt/sonic-pi/etc/samples/elec_soft_kick.wav',
  9: '/opt/sonic-pi/etc/samples/elec_tick.wav',
  10: '/opt/sonic-pi/etc/samples/vinyl_rewind.wav',
  11: '/opt/sonic-pi/etc/samples/elec_twang.wav',
  12: '/usr/share/scratch/Media/Sounds/Animal/Bird.wav',
  13: '/usr/share/scratch/Media/Sounds/Animal/Cricket.wav',
  14: '/usr/share/scratch/Media/Sounds/Animal/Dog1.wav',
  15: '/usr/share/scratch/Media/Sounds/Animal/Dog2.wav',
  16: '/usr/share/scratch/Media/Sounds/Animal/Duck.wav',
  17: '/usr/share/scratch/Media/Sounds/Animal/Goose.wav',
  18: '/usr/share/scratch/Media/Sounds/Animal/Horse.wav',
  19: '/usr/share/scratch/Media/Sounds/Animal/Kitten.wav',
  20: '/usr/share/scratch/Media/Sounds/Animal/Meow.wav',
  21: '/usr/share/scratch/Media/Sounds/Animal/Owl.wav',
  22: '/usr/share/scratch/Media/Sounds/Animal/Rooster.wav',
  23: '/usr/share/scratch/Media/Sounds/Animal/WolfHowl.wav',
}


sounds = [0]*len(SOUND_MAPPING.keys())

for key,soundfile in SOUND_MAPPING.iteritems():
        sounds[key] =  pygame.mixer.Sound(soundfile)
        sounds[key].set_volume(1);

shutdown_command = '/usr/bin/sudo /sbin/shutdown -r now'

# Main loop to print a message every time a pin is touched.
print('Press Ctrl-C to quit.')
last_touched = cap.touched()
offset = 0
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
            print('{0} touched!'.format(i))
            if i == 11:
                offset += 12
                offset = offset % len(SOUND_MAPPING.keys())
                print('changing offset to {0}'.format(offset)) 
            if i == 10:
                subprocess.Popen(shutdown_command.split())
            if (sounds[i + offset]):
                print('playing sound {0}'.format(i + offset))
                sounds[i + offset].play()
        
        if not current_touched & pin_bit and last_touched & pin_bit:
            print('{0} released!'.format(i))

    # Update last state and wait a short period before repeating.
    last_touched = current_touched
    time.sleep(0.1)

    # Alternatively, if you only care about checking one or a few pins you can
    # call the is_touched method with a pin number to directly check that pin.
    # This will be a little slower than the above code for checking a lot of pins.
    #if cap.is_touched(0):
    #    print('Pin 0 is being touched!')

    # If you're curious or want to see debug info for each pin, uncomment the
    # following lines:
    #print('\t\t\t\t\t\t\t\t\t\t\t\t\t 0x{0:0X}'.format(cap.touched()))
    #filtered = [cap.filtered_data(i) for i in range(12)]
    #print('Filt:', '\t'.join(map(str, filtered)))
    #base = [cap.baseline_data(i) for i in range(12)]
    #print('Base:', '\t'.join(map(str, base)))

#!/usr/bin/env python3

import time
from rpi_ws281x import *
import argparse

# LED strip configuration:
LED_COUNT      = 1      # Number of LED pixels.
LED_PIN        = 18      # GPIO pin connected to the pixels (18 uses PWM!).
#LED_PIN        = 10      # GPIO pin connected to the pixels (10 uses SPI /dev/spidev0.0).
LED_FREQ_HZ    = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA        = 10      # DMA channel to use for generating signal (try 10)
LED_BRIGHTNESS = 150     # Set to 0 for darkest and 255 for brightest
LED_INVERT     = False   # True to invert the signal (when using NPN transistor level shift)
LED_CHANNEL    = 0       # set to '1' for GPIOs 13, 19, 41, 45 or 53
LED_DEFAULT_COLOR = Color(120,50,50) # default color for neopixel

def initiateNeopixel():

        # Create NeoPixel object with appropriate configuration.
    neopixel = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL)
    # Intialize the library (must be called once before other functions).
    neopixel.begin()
    return neopixel


def clearNeopixel(neopixel):

    neopixel.setPixelColor(0,Color(0,0,0))
    neopixel.show()
    return

def neopixelOn(neopixel, rgb=LED_DEFAULT_COLOR):

    neopixel.setPixelColor(0,rgb)    
    neopixel.show()

def flash(neopixel, rgb=LED_DEFAULT_COLOR, pause=.5, number=10):

    count=0
    while count<number:
  
        clearNeopixel(neopixel)
        neopixel.show()
        time.sleep(pause)
        neopixel.setPixelColor(0,rgb)
        neopixel.show()
        time.sleep(pause)
        count+=1

    clearNeopixel(neopixel)

    return

    
# Main program logic follows:
if __name__ == '__main__':
    # Process arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--clearNeopixel', action='store_true', help='clearNeopixel the display on exit')
    args = parser.parse_args()

    # Create NeoPixel object with appropriate configuration.
    neopixel = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL)
    # Intialize the library (must be called once before other functions).
    neopixel.begin()

    print ('Press Ctrl-C to quit.')
    if not args.clearNeopixel:
        print('Use "-c" argument to clearNeopixel LEDs on exit')

    try:

#        flash(neopixel)
        neopixelOn(neopixel)
        time.sleep(2)
        clearNeopixel(neopixel)

    except KeyboardInterrupt:
        if args.clearNeopixel:
            colorWipe(neopixel, Color(0,0,0), 10)



'''utility to test battery life for lipo shim'''

import RPi.GPIO as GPIO
import time
import logger
import datetime

def get_pin_state():

    GPIO.setmode(GPIO.BCM)
    GPIO.setup(4, GPIO.IN)

    state = GPIO.input(4)
    return state

logfile = logger.loggerMaster('battery_test','battery.log',logLevel="DEBUG")



while True:

    logfile.info(str(get_pin_state()))
    time.sleep(5)

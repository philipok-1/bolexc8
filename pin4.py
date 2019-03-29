'''utility to test battery life for lipo shim'''

import RPi.GPIO as GPIO
import time
import logger
import datetime

logfile = logger.loggerMaster('battery_test','bolexc8.log',logLevel="DEBUG")

INTERVAL=10

def get_pin_state():

    GPIO.setmode(GPIO.BCM)
    GPIO.setup(4, GPIO.IN)

    state = GPIO.input(4)
    return state


def main():

    timenow=time.time()


    while True:
        if time.time()-timenow>INTERVAL:

            logfile.info(str(get_pin_state()))
            timenow=time.time()
        else:
            pass    


if __name__=='__main__':

    main()

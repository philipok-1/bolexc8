#!/usr/bin/env python 

'''incorporated config feature
matched actual fps to ffmpeg conversion rate'''

#imports

from gpiozero import Button, LED
import time
import logger

#set up logging

logfile = logger.loggerMaster('button','button.log',logLevel="DEBUG")

#set up physical devices

button = Button(16)


def main():

    while True:

        while button.is_pressed:

            logfile.info("Button pressed")
            time.sleep(2)

        else: pass

if __name__ == "__main__":

    main()

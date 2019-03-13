#!/usr/bin/env python 

'''incorporated config feature
matched actual fps to ffmpeg conversion rate'''

#imports

import os, sys
import subprocess
import time, datetime
import shutil
import configparser
import numpy as np
import cv2
from gpiozero import Button, LED
import urllib.request,urllib.parse,urllib.error
import logger

#set up logging

logfile = logger.loggerMaster('bolexc8','bolexc8.log',logLevel="DEBUG")

#set up physical devices

button = Button(22)
led=LED(17)

#import configuration settings

config = configparser.ConfigParser()
config.read('config.ini')
logfile.info ("reading config file")

email=config['comms']['Email']
max_film_time=config['filming']['max_time']
file_location=config['filming']['file_location']

#filming timer

COUNT=0

#maximum time in seconds of filming

TIMER=25

#camera mode

camera_mode="idle"

#helper functions

def flash_led(device, times=3, frequency=.05):

    count=0
    while count<(times+1):

        device.toggle()
        count+=1
        time.sleep(frequency)
    device.off()
    return

def indicate_ready(clear=True):
    
    if clear: os.system('clear')
    logfile.info ("BolexC8 Retrofit....  (C) PBW 2019..\n")
    flash_led(led, 10)
    logfile.info ("ready")

def check_connectivity():

    '''pings google to determine internet connectivity (True/False)'''

    try:
        urllib.request.urlopen('http://216.58.192.142', timeout=1)
        return True
    except urllib.error.URLError as err: 
        logfile.warning("No internet connection for file transfer")
        return False

def send_file(filename, file, email):

    '''emails a file to defined address'''

    led.on()
    subprocess.call(["mpack", "-s", str(filename) ,file," bolexc8@gmail.com"], shell=False)
    time.sleep(2)
    led.off()

    return

def convert_video(input_file, framerate=20):

    framerate=str(framerate)
    timestr = time.strftime("%Y%m%d-%H%M%S")
    filename=str(input_file)
#    subprocess.check_output(['ffmpeg','-nostats' ,'-loglevel','0','-r','20', '-i', filename, '-b:a', '128k', '-c:v', 'libx264','-crf', '23',  timestr+".mp4"], shell=False)    
    subprocess.check_output(['ffmpeg','-r',framerate, '-i', filename, '-b:a', '128k', '-c:v', 'libx264','-crf', '23',  timestr+".mp4"], shell=False)
    logfile.info ("conversion complete")
    return


def move_file(file, destination):

    '''file move utility using shutil'''

    current_file=file
    destination_file=destination

    shutil.move("/home/pi/scripts/c8/"+current_file, "/home/pi/scripts/c8/archive/"+destination_file)


def scan_directory(source=str(file_location), filetype='.mp4'):

    '''scans the defined directory and emails video, then archives it'''

    logfile.info ("starting scan")

    directory = os.fsencode(source)

    for file in os.listdir(directory):
        filename = os.fsdecode(file)
        if filename.endswith(filetype):
            send_file(filename, str(source+filename), email)
            move_file(filename, filename)
            continue
        else:
            continue

    logfile.info("finished scanning "+str(directory))

    return

#main function

def film(COUNT=COUNT, TIMER=max_film_time):
    
    '''this is the function that takes the video'''

#set capture device

    global camera_mode

    cap = cv2.VideoCapture(0)

    if cap is None or not cap.isOpened():

        logfile.warning("No camera detected")
        sys.exit()

#measure script execution time

    time_elapsed=time.time()

#set up video output

    timestr = time.strftime("%Y%m%d-%H%M%S")

    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    filename=timestr+'.avi'
    out = cv2.VideoWriter(filename,fourcc, 20.0, (640,480))

    while(True):

    # Capture frame-by-frame
        ret, frame = cap.read()

    #write video to file

        out.write(frame)

    # Display frame - NB eventually remove this to improve frame rate
        cv2.imshow('frame', frame)
       
    #increment count

        COUNT+=1
        flash=COUNT

    #flash LED every second
        if flash%10==0:
           led.toggle()

    #exit 

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

        if COUNT==(TIMER*10):
            break

        if button.is_pressed==False:

            camera_mode=False
            break

    # done - capture release

    total_time=time.time()-time_elapsed
    fps=int(COUNT//total_time)
    logfile.info ("total time="+str(total_time))
    logfile.info ("frames/second="+str(fps))

    led.off()
    cap.release()
    cv2.destroyAllWindows()

    #start processing the video

    led.on()
    logfile.info ("converting avi")
    convert_video('/home/pi/scripts/c8/'+filename, fps)
    #send pics
    scan_directory()
    led.off()
    indicate_ready()

    return

#main script

def main():

    indicate_ready()

    scan_directory()

    while True:

        if button.is_pressed:

            if button.is_held:

               camera_mode="active"
               button_count=0

        else: camera_mode="idle"

        if camera_mode=="active":

            film()

if __name__ == "__main__":

    main()

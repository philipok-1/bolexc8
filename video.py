#!/usr/bin/env python 

#workingon config

import os
import subprocess
import time, datetime
import shutil
import configparser
import numpy as np
import cv2
from gpiozero import Button, LED
import urllib.request,urllib.parse,urllib.error

#set up physical devices

button = Button(22)
led=LED(17)

#filming time constants

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


def check_connectivity():

    '''pings google to determine internet connectivity (True/False)'''

    try:
        urllib.request.urlopen('http://216.58.192.142', timeout=1)
        return True
    except urllib.error.URLError as err: 
        return False

def send_file(filename, file):

    '''emails a file to defined address'''

    led.on()
    subprocess.call(["mpack", "-s", str(filename) ,file," bolexc8@gmail.com"], shell=False)
    time.sleep(2)
    led.off()

    return

def convert_video(input_file):

    timestr = time.strftime("%Y%m%d-%H%M%S")
    filename=str(input_file)
#    subprocess.check_output(['ffmpeg','-nostats' ,'-loglevel','0','-r','20', '-i', filename, '-b:a', '128k', '-c:v', 'libx264','-crf', '23',  timestr+".mp4"], shell=False)    
    subprocess.check_output(['ffmpeg','-r','20', '-i', filename, '-b:a', '128k', '-c:v', 'libx264','-crf', '23',  timestr+".mp4"], shell=False)
    print ("conversion complete")
    return


def move_file(file, destination):

    '''file move utility using shutil'''

    current_file=file
    destination_file=destination

    shutil.move("/home/pi/scripts/c8/"+current_file, "/home/pi/scripts/c8/archive/"+destination_file)


def scan_directory(source='/home/pi/scripts/c8/', filetype='.mp4'):

    '''scans the defined directory and emails video, then archives it'''

    print ("starting scan")

    directory = os.fsencode(source)

    for file in os.listdir(directory):
        filename = os.fsdecode(file)
        if filename.endswith(filetype):
            send_file(filename, str(source+filename))
            move_file(filename, filename)
            continue
        else:
            continue

    return

#main function

def film(COUNT=COUNT, TIMER=TIMER):
    
    '''this is the function that takes the video'''

#set capture device

    global camera_mode

    cap = cv2.VideoCapture(0)

#measure script execution time

    time_elapsed=time.time()

#set up video output

    timestr = time.strftime("%Y%m%d-%H%M%S")

    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    filename=timestr+'.avi'
    out = cv2.VideoWriter(filename,fourcc, 20.0, (640,480))

#screen text (for debugging)

    font                   = cv2.FONT_HERSHEY_SIMPLEX
    bottomLeftCornerOfText = (10,250)
    fontScale              = 1
    fontColor              = (255,255,255)
    lineType               = 2

    while(True):

    # Capture frame-by-frame
        ret, frame = cap.read()

    # write text to frame
#    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
#    cv2.putText(frame,str(COUNT), bottomLeftCornerOfText, 
 #   font, 
  #  fontScale,
   # fontColor,
    #lineType)

    #write video to file

        out.write(frame)

    # Display frame - NB remove this to improve frame rate
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
    print ("total time="+str(total_time))
    print ("frames/second="+str(COUNT/total_time))

    led.off()
    cap.release()
    cv2.destroyAllWindows()

    #start processing the video

    led.on()
    print ("converting avi")
    convert_video('/home/pi/scripts/c8/'+filename)
    #send pics
    scan_directory()
    led.off()
    indicate_ready()

    return

#main script

def indicate_ready(clear=True):
    
    if clear: os.system('clear')
    print ("BolexC8 Retrofit....  (C) PBW 2019..\n")
    flash_led(led, 10)
    print ("ready")


indicate_ready()

config = configparser.ConfigParser()
config.read('config.ini')
print (config.sections())
print (config['comms']['Email'])

while True:

    if button.is_pressed:

       if button.is_held:

           camera_mode="active"
           button_count=0

    else: camera_mode="idle"

    if camera_mode=="active":

        film()

    

    

#testing stash

import os
import subprocess
import time, datetime
import shutil
import numpy as np
import cv2
from gpiozero import Button, LED
import urllib.request,urllib.parse,urllib.error

#physical devices

button = Button(22)
led=LED(17)

#filming time constants

COUNT=0
TIMER=25

#camera mode

camera_mode="idle"

#main functions

def flash_led(device, times=3, frequency=.05):

    count=0
    while count<(times+1):

        device.toggle()
        count+=1
        time.sleep(frequency)
    device.off()
    return
        

def check_connectivity():

    try:
        urllib.request.urlopen('http://216.58.192.142', timeout=1)
        return True
    except urllib.error.URLError as err: 
        return False

def send_file(filename, file):

    led.on()
    subprocess.Popen(["mpack", "-s", str(filename) ,file," XXXX@gmail.com"], shell=False)
    time.sleep(2)
    led.off()

    return

def move_file(file, destination):

    current_file=file
    destination_file=destination

    shutil.move("/home/pi/scripts/c8/"+current_file, "/home/pi/scripts/c8/archive/"+destination_file)


def iterate_directory(source='/home/pi/scripts/c8/', filetype='.avi'):

    directory = os.fsencode(source)

    for file in os.listdir(directory):
        filename = os.fsdecode(file)
        if filename.endswith(filetype):
            send_file(filename, str(source+filename))
#            move_file(filename, filename)
            continue
        else:
            continue

def film(COUNT=COUNT, TIMER=TIMER):
    
    global camera_mode

    cap = cv2.VideoCapture(0)

#measure script execution time

    time_elapsed=time.time()

#set up video output

    timestr = time.strftime("%Y%m%d-%H%M%S")

    fourcc = cv2.VideoWriter_fourcc(*'XVID')

    out = cv2.VideoWriter(timestr+'.avi',fourcc, 20.0, (640,480))
#    out = cv2.VideoWriter(timestr+'.avi',fourcc, 20.0, (1280,720))

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
#        out.write(frame)

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
    #send pics
    iterate_directory()

    return

#main script

flash_led(led, 10)
print ("ready")


while True:

    if button.is_pressed:

       if button.is_held:

           camera_mode="active"
           button_count=0

    else: camera_mode="idle"

    if camera_mode=="active":

        film()

    

    

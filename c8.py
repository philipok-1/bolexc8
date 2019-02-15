from gpiozero import Button

import subprocess

button = Button(17)

recording=False
DURATION=10

#ffmpeg -f v4l2 -i /dev/video0 -t 01:00:00 output

def record(time=DURATION):

    subprocess.Popen(['ffmpeg -t 00:00:10 /home/pi/scripts/c8/'], shell=True)

record()

#while True:
 #   if button.is_pressed:
  #      print("Button is pressed")
   # else:
    #    print("Button is not pressed")

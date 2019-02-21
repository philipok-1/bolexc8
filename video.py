import numpy as np
import time
import cv2
from gpiozero import Button, LED

button = Button(22)
led=LED(17)

cap = cv2.VideoCapture(0)

#filming time constants

COUNT=0
TIMER=25

#measure script execution time

time_elapsed=time.time()

#set up video output

timestr = time.strftime("%Y%m%d-%H%M%S")

fourcc = cv2.VideoWriter_fourcc(*'XVID')
out = cv2.VideoWriter(timestr+'.avi',fourcc, 20.0, (640,480))

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
    #out.write(frame)

    # Display frame
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

# done - capture release

total_time=time.time()-time_elapsed
print ("total time="+str(total_time))
print ("frames/second="+str(COUNT/total_time))

cap.release()
cv2.destroyAllWindows()


import subprocess
import time



def convert_video(input_file):

    timestr = time.strftime("%Y%m%d-%H%M%S")
    filename=str(input_file)
    subprocess.call(['ffmpeg','-nostats' ,'-loglevel','0', '-r','20', '-i', filename, '-b:a', '128k', '-c:v', 'libx264','-crf', '23',  timestr+".mp4"], shell=False)    
    print ("conversion complete")

    return


convert_video('20190304-183220.avi')

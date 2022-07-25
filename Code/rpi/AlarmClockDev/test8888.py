import alarmClock as ac
import pigpio
from signal import pause
from time import sleep
from datetime import datetime

from signal import signal, SIGINT
from sys import exit

CS1    = 7
NUMPIX = 86
BRIGHT = 255 #RANGE: 224-255

pi = pigpio.pi()
pi.set_mode(CS1, pigpio.OUTPUT)
pi.write(CS1,0)

strand = pi.spi_open(1,32000,3)

clockface = ac.apa102ClockDisplay('red',2)

def updateClock():
    framebuffer = [0,0,0,0]
    framebuffer.extend(clockface.writeOut())
    framebuffer.extend([255,255,255,255,255,255,255,255])
    pi.write(CS1,1)
    pi.spi_write(strand, framebuffer)
    pi.write(CS1,0)

def handler(signal_received, frame):
    # Handle any cleanup here
    print('SIGINT or CTRL-C detected. Exiting gracefully')
    clockface.setOff()
    updateClock()
    updateClock()
    pi.spi_close(strand)
    exit(0)

if __name__ == '__main__':
    # Tell Python to run the handler() function when SIGINT is recieved
    signal(SIGINT, handler)
    print('Running. Press CTRL-C to exit.')
    while True:
        now = datetime.now()
        timestr = ""
        if (int(now.strftime("%-I")) < 10):
            timestr = " "+now.strftime("%-I:%M")
        else:
            timestr = now.strftime("%-I:%M")
        print(timestr)
        timestr = "88:88"
        clockface.setTime(timestr)
        updateClock()
        sleep(1)

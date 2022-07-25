import alarmClock as ac
import pigpio
from signal import pause
from time import sleep

CS1    = 7
NUMPIX = 86
BRIGHT = 255 #RANGE: 224-255

pi = pigpio.pi()
pi.set_mode(CS1, pigpio.OUTPUT)
pi.write(CS1,0)

strand = pi.spi_open(1,32000,3)

def sendDigitInColor(digit, color):
    testDigit = ac.apa1027SegDigit()
    testDigit.setColor(color)
    framebuffer = [0,0,0,0]
    framebuffer.extend(testDigit.writeOutDigit(digit))
    framebuffer.extend([255,255,255,255])

    pi.write(CS1,1)
    pi.spi_write(strand, framebuffer)
    pi.write(CS1,0)

index = 0;
while True:
    sendDigitInColor(index,'bayern')
    index = index + 1
    if (index > 10): index = 0
    sleep(1)

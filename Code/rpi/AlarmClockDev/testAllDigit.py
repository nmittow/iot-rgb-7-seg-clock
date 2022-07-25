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
    testDigit0 = ac.apa1027SegDigit()
    testDigit1 = ac.apa1027SegDigit()
    colon0     = ac.apa102pixel()
    colon1     = ac.apa102pixel()
    testDigit2 = ac.apa1027SegDigit()
    testDigit3 = ac.apa1027SegDigit()
    testDigit0.setColor(color)
    testDigit1.setColor(color)
    colon0.setColor(color)
    colon1.setColor(color)
    testDigit2.setColor(color)
    testDigit3.setColor(color)
    framebuffer = [0,0,0,0]
    framebuffer.extend(testDigit0.writeOutDigit(digit))
    framebuffer.extend(testDigit1.writeOutDigit(digit))
    framebuffer.extend(colon0.writeOut())
    framebuffer.extend(colon1.writeOut())
    framebuffer.extend(testDigit2.writeOutDigit(digit))
    framebuffer.extend(testDigit3.writeOutDigit(digit))
    framebuffer.extend([255,255,255,255])
    framebuffer.extend([255,255,255,255])

    pi.write(CS1,1)
    pi.spi_write(strand, framebuffer)
    pi.write(CS1,0)

index = 0;
while True:
    sendDigitInColor(index,'burntorange')
    index = index + 1
    if (index > 10): index = 0
    sleep(1)

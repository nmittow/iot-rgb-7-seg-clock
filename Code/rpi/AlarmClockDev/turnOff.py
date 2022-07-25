#  strandTest.py
#
#  For a strand of APA102 LEDs
#
#  nmittow@protonmail.ch  
#
#  Reference for APA102 thats legible: http://www.smythe-consulting.com/2017/03/driving-dotstar-apa102-led-strings-with.html
#
#

import pigpio
from signal import pause
from time import sleep

CS1    = 7
NUMPIX = 86
BRIGHT = 255 #RANGE: 224-255

pi = pigpio.pi()
pi.set_mode(CS1, pigpio.OUTPUT)
pi.write(CS1,0)

strand = pi.spi_open(1,50000,1)

def sendSingleColor(b,g,r):
    pi.write(CS1,1)
    pi.spi_write(strand, [0,0,0,0])
    for i in range(NUMPIX):
        pi.spi_write(strand,[BRIGHT,b,g,r])
    n = NUMPIX
    while (n > 0):
        pi.spi_write(strand, [255,255,255,255])
        n = n - 64
    pi.write(CS1,0)

pi.write(CS1,1)
pi.spi_write(strand, [0,0,0,0])
for i in range(NUMPIX):
    pi.spi_write(strand,[224,0,0,0])
n = NUMPIX
while (n > 0):
    pi.spi_write(strand, [255,255,255,255])
    n = n - 64
    pi.write(CS1,0)
    

#while (True):
#    sendSingleColor(255,0,0)
#    sleep(1)
#    sendSingleColor(0,255,0)
#    sleep(1)
#    sendSingleColor(0,0,255)
#    sleep(1)

#pi.write(CS1,1)
#pi.spi_write(strand,[0,0,0,0])
#pi.spi_write(strand,[255,255,0,0])
#pi.write(CS1,0)

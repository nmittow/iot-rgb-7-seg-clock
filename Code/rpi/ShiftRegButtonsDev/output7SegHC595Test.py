import pigpio
from signal import pause
import time

CS1    = 7

pi = pigpio.pi()
pi.set_mode(CS1, pigpio.OUTPUT)
pi.write(CS1,1)

hc595 = pi.spi_open(1,50000,0)

def intTo7SegByte(num):
    if   num == 0:
        return 0b00111111
    elif num == 1:
        return 0b00000110
    elif num == 2:
        return 0b01011011
    elif num == 3:
        return 0b01001111
    elif num == 4:
        return 0b01100110
    elif num == 5:
        return 0b01101101
    elif num == 6:
        return 0b01111101
    elif num == 7:
        return 0b00000111
    elif num == 8:
        return 0b01111111
    elif num == 9:
        return 0b01101111
    else:
        return 0b10000000

def writeDigitToReg(num):
    pi.write(CS1,0)
    code = intTo7SegByte(num)
    testcode = [0,0,0,0,0,0,0,1]
    print("preparing to write: %d" % code)
    pi.spi_write(hc595, [code])
    #pi.spi_write(hc595, testcode)
    pi.write(CS1,1)

count = 0;
while 1:
    if count > 10:
        count = 0
    print(count)
    writeDigitToReg(count)
    count=count+1
    time.sleep(1)

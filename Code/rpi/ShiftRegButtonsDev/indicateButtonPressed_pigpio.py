import pigpio
from signal import pause

SHLD   = 25
BTNINT = 4
CS1    = 7

pi = pigpio.pi()
pi.set_mode(BTNINT, pigpio.INPUT)
pi.set_mode(SHLD, pigpio.OUTPUT)
pi.set_mode(CS1, pigpio.OUTPUT)
pi.write(SHLD,0)
pi.write(CS1,0)

hc165 = pi.spi_open(0,50000,2)
hc595 = pi.spi_open(0,50000,0)

def intTo7SegByte(num):
    if   num == 0:
        return 0b01111110
    elif num == 1:
        return 0b00001100
    elif num == 2:
        return 0b10110110
    elif num == 3:
        return 0b10011110
    elif num == 4:
        return 0b11001100
    elif num == 5:
        return 0b11011010
    elif num == 6:
        return 0b11111010
    elif num == 7:
        return 0b00001110
    elif num == 8:
        return 0b11111110
    elif num == 9:
        return 0b11001110
    else:
        return 0b00000001

def writeDigitToReg(num):
    pi.write(CS1,1)
    code = intTo7SegByte(num)
    testcode = [1,0,0,0,0,0,0,0]
    print("preparing to write: %d" % code)
    pi.spi_write(hc595, testcode)
    #pi.spi_write(hc595, testcode)
    pi.write(CS1,0)

def decodeButtons(byte):
    if   byte == 1:
        return 1
    elif byte == 2:
        return 2
    elif byte == 4:
        return 3
    elif byte == 8:
        return 4
    elif byte == 16:
        return 5
    elif byte == 32:
        return 6
    elif byte == 64:
        return 7
    elif byte == 128:
        return 8
    else:
        return -1

def buttonPressed(gpio,level,tick):
    pi.write(SHLD,1)
    (numbytes, bytearr) = pi.spi_read(hc165, 1)
    bnum = decodeButtons(bytearr[0])
    print(bytearr)
    if (numbytes == 1):
        print("BUTTON: %d PRESSED" % bnum)
    else:
        print("ERROR: BYTES READ: %d" % numbytes)
    pi.write(SHLD,0)
    writeDigitToReg(bnum)

triggercb = pi.callback(BTNINT,pigpio.RISING_EDGE,buttonPressed)
pause()

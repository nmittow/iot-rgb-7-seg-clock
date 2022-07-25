
from gpiozero import *
from signal import pause

shld  = DigitalOutputDevice(25)
hc165 = SPIDevice()

def read_shiftreg():
    print("a button was pushed")
    shld.on()
    print(hc165._spi.transfer(0b00000000))
    shld.off()


buttonTrigger = Button(4)
buttonTrigger.when_released = read_shiftreg

pause()


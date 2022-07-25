import pigpio
from signal import pause
from time import sleep

usleep = lambda x: sleep(x/1000000.0)

S = 23
R = 22

pi = pigpio.pi()
pi.set_mode(S, pigpio.OUTPUT)
pi.set_mode(R, pigpio.OUTPUT)

pi.write(S,0)
pi.write(R,0)


while True:
    pi.write(S, 1)
    sleep(1)
    pi.write(S, 0)
    sleep(2)
    pi.write(R, 1)
    sleep(1)
    pi.write(R, 0)
    sleep(2)

        

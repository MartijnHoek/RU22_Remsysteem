from encoder import Encoder
import RPi.GPIO as GPIO

import PID_RU22

import DOGA_RU22

DOGA = DOGA_RU22.DOGA(32,37,100)

GPIO.setmode(GPIO.BOARD)

PID = PID_RU22.PIDC(1,0,0,-100,100)

A = 16
B = 13
angle = 0
e1 = Encoder(A,B)

PID.spcalc(20)

while True: 
        
        angle = e1.getValue()
        #print(angle)
        print(angle)
        
        
        PID.pidexc(angle)
        
        PID.get_pwm()

        DOGA.motor_aansturen(PID.pwm)

        if PID.pwm == 0:
            PID.spcalc(input('input svp'))

from encoder import Encoder
import RPi.GPIO as GPIO

from simple_pid import PID

import PID_RU22

from time import sleep

import DOGA_RU22

DOGA = DOGA_RU22.DOGA(32,37,100)

GPIO.setmode(GPIO.BOARD)

PID = PID_RU22.PIDC(1,0,0,-100,100)

A = 16
B = 13
angle = 0
e1 = Encoder(A,B)

PID.spcalc(10)

# AN1 = 32
# DIG1 = 37

#GPIO.setup(AN1, GPIO.OUT)		# set pin as output
#GPIO.setup(DIG1, GPIO.OUT)		# set pin as output
#p1 = GPIO.PWM(AN1, 100)			# set pwm for M1

while True: 
        
        angle = e1.getValue() * (360/972)
        #print(angle)
        
        PID.pidexc(angle)
        
        PID.get_pwm()

        DOGA.motor_aansturen(PID.pwm)

        if PID.pwm == 0:
            PID.spcalc(input('input svp'))
#         if PID.pwm <= 0:  #and PID.a <= 0:
#             GPIO.output(DIG1, GPIO.HIGH)		# set DIG1 as HIGH, M1B will turn ON
#             p1.start(abs(PID.pwm))			# set speed for M1 at 100%
# 
# 
#         if PID.pwm >= 0: #and PID.a >= 0:
#             GPIO.output(DIG1, GPIO.LOW)		# set DIG1 as HIGH, M1B will turn ON
#             p1.start(abs(PID.pwm))			# set speed for M1 at 100%
            
#         while PID.gw >= angle:  #and PID.a <= 0:
#             GPIO.output(DIG1, GPIO.HIGH)		# set DIG1 as HIGH, M1B will turn ON
#             p1.start(abs(PID.pwm))			# set speed for M1 at 100%
#             angle = e1.getValue() * (360/972)
#             PID.pidexc(angle)
#             PID.get_pwm()
#             
#         while PID.gw <= angle: #and PID.a >= 0:
#             GPIO.output(DIG1, GPIO.LOW)		# set DIG1 as HIGH, M1B will turn ON
#             p1.start(abs(PID.pwm))			# set speed for M1 at 100%
#             angle = e1.getValue() * (360/972)
#             PID.pidexc(angle)
#             PID.get_pwm()
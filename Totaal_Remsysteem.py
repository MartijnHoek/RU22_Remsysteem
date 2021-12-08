# Startup 
import keyboard                 # Importeert keyboard library
import time
import board
import busio
import digitalio
import pulseio
import adafruit_ads1x15.ads1015 as ADS
from adafruit_ads1x15.analog_in import AnalogIn

# Analoog / Digitaal Converter
i2c = busio.I2C(board.SCL, board.SDA)
ads = ADS.ADS1015(i2c)
chan1 = AnalogIn(ads, ADS.P0)
chan2 = AnalogIn(ads, ADS.P1)

# Motor aansturing
dir1 = digitalio.DigitalInOut(board.D26)
dir2 = digitalio.DigitalInOut(board.D24)
dir1.direction = digitalio.Direction.OUTPUT
dir2.direction = digitalio.Direction.OUTPUT
PWM = pulseio.PWMOut(board.D12)

class Remdruksensor:    
    def __init__(self, chan1, chan2):
        self.chan1 = chan1
        self.chan2 = chan2

    def meet(self):
        meetwaarde = round(chan1.voltage,2),round(chan2.voltage,2),\
             int(chan1.voltage/(chan1.voltage+chan2.voltage)*100), int(chan2.voltage/(chan1.voltage+chan2.voltage)*100)
        return meetwaarde

class Keyboard:
    def __init__ (self, PWM):
        self.PWM =  PWM
        self.block = True
        self.display = True
        
    def motor_uit(self):
        PWM.duty_cycle = 0
        print("Motor Uit")       
        dir1.value = True
        dir2.value = False       
        
    def motor_aan(self):
        PWM.duty_cycle = 65535
        print("Motor Aan")        
        dir1.value = True
        dir2.value = False
        
    def Press(self):
        if self.block == False:              # Wanneer waarde block gelijk is aan False open loop
            print("Werkt")
            self.display = not self.display  # De waarde van Display wordt omgedraaid True -> False en andersom  dit is belangrijk voor de onderstaande IF loop
            self.block = True                # Waarde van Block wordt True zodat loop niet opnieuw opend


Signalen_Remdruksensor = Remdruksensor(chan1, chan2)
   
eigen_keyboard = Keyboard(0)
   
while True:  
        
    if keyboard.is_pressed("k"):        # Wanneer toets k ingedrukt open loop      
       eigen_keyboard.Press()
    else: 
        eigen_keyboard.block = False                   # Block wordt terug op False gezet
    if eigen_keyboard.display:                         # Als Display True is opend deze loop
        eigen_keyboard.motor_uit()      
    else:                               # Als Display False is opend deze loop
        eigen_keyboard.motor_aan()

    print(Signalen_Remdruksensor.meet())

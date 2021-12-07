import time
import board
import busio
import adafruit_ads1x15.ads1015 as ADS
from adafruit_ads1x15.analog_in import AnalogIn

i2c = busio.I2C(board.SCL, board.SDA)

ads = ADS.ADS1015(i2c)

chan1 = AnalogIn(ads, ADS.P0)
chan2 = AnalogIn(ads, ADS.P1)

class Remdruksensor:    
    def __init__(self, chan1, chan2):
        self.chan1 = chan1
        self.chan2 = chan2

    def meet(self):
        meetwaarde = round(chan1.voltage,2),round(chan2.voltage,2),\
             int(chan1.voltage/(chan1.voltage+chan2.voltage)*100), int(chan2.voltage/(chan1.voltage+chan2.voltage)*100)
        return meetwaarde

Signalen_Remdruksensor = Remdruksensor(chan1, chan2)
      
while True:

    print(Signalen_Remdruksensor.meet())
        

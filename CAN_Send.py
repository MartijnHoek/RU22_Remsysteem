#sudo /sbin/ip link set can0 up type can bitrate 500000 # Instellingen voor setup CAN-bus

# Startup (libraries)
import cantools
import can
from can.message import Message

import time                                          # Importeert time library      (RPi)
import board                                         # Importeert board library     (adafruit)
import busio                                         # Importeert busio library     (adafruit)
import adafruit_ads1x15.ads1015 as ADS               # Importeert ADS library       (adafruit)
from adafruit_ads1x15.analog_in import AnalogIn      # Importeer AnalogIn library   (adafruit)

# Analoog / Digitaal Converter
i2c = busio.I2C(board.SCL, board.SDA)                # busio.I2C creeert een interface voor de I2C protocol
ads = ADS.ADS1015(i2c)                               # De ADS drive wordt aangegeven welke interface toegepast moet worden
chan1 = AnalogIn(ads, ADS.P0)                        # De toegepaste kanalen op de ADC worden gedefineerd
chan2 = AnalogIn(ads, ADS.P1)                        # De toegepaste kanalen op de ADC worden gedefineerd

class Remdruksensor:                                 # Klasse voor de remdruksensor wordt aangemaakt
    def __init__(self, chan1, chan2):                # De klasse wordt geinitialiseerd
        self.chan1 = chan1                           # Kanaal 1 wordt aangeduid
        self.chan2 = chan2                           # Kanaal 2 wordt aangeduid

    def meet(self):                                  # De meet klasse wordt aangemaakt, in deze klasse wordt het analoge signal omgezet naar digitaal.
        meetwaarde = round(chan1.voltage,2),round(chan2.voltage,2),\
             int(chan1.voltage/(chan1.voltage+chan2.voltage)*100), int(chan2.voltage/(chan1.voltage+chan2.voltage)*100)
        return meetwaarde

Signalen_Remdruksensor = Remdruksensor(chan1, chan2)

db = cantools.db.load_file('/home/pi/RU22_Remsysteem/Test_DBC_Files.dbc')
msg = db.get_message_by_name('Test_berichten')
bus = can.interface.Bus(channel='can0', bustype='socketcan_native')

def arduino_map(x, in_min, in_max, out_min, out_max):
    return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min

while True:

    Sensor1Voltage = chan1.voltage
    Sensor2Voltage = chan2.voltage
    
    Sensor1Stand = arduino_map(chan1.voltage, 0, 3.3, 0, 255)
    Sensor2Stand = arduino_map(chan2.voltage, 0, 3.3, 0, 255)

    msg_data = msg.encode({'Pot1':Sensor1Stand, 'Pot2':Sensor2Stand})
    bericht=can.Message(arbitration_id=msg.frame_id, data=msg_data)
    bus.send(bericht) 
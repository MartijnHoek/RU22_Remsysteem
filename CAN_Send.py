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

def arduino_map(x, in_min, in_max, out_min, out_max):
    return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min

class Remdruksensor:                                 # Klasse voor de remdruksensor wordt aangemaakt
    def __init__(self, chan1, chan2):                # De klasse wordt geinitialiseerd
        self.chan1 = chan1                           # Kanaal 1 wordt aangeduid
        self.chan2 = chan2                           # Kanaal 2 wordt aangeduid

Signalen_Remdruksensor = Remdruksensor(AnalogIn(ads, ADS.P0),AnalogIn(ads,ADS.P1))       
  
bus = can.interface.Bus(channel='can0', bustype='socketcan_native')
db = cantools.db.load_file('/home/pi/RU22_Remsysteem/Test_DBC_Files.dbc')
Test_berichten = db.get_message_by_name('Test_berichten')
 
while True:
   
    Sensor1Stand = arduino_map(Signalen_Remdruksensor.chan1.voltage, 0, 3.3, 0, 255)
    Sensor2Stand = arduino_map(Signalen_Remdruksensor.chan2.voltage, 0, 3.3, 0, 255)

    Test_berichten_data = Test_berichten.encode({'Pot1':Sensor1Stand, 'Pot2':Sensor2Stand})
    Test_berichten_bericht=can.Message(arbitration_id=Test_berichten.frame_id, data=Test_berichten_data)
    bus.send(Test_berichten_bericht)
    
    message = bus.recv()
    message=db.decode_message(message.arbitration_id, message.data) 
    Test_berichten_Pot1=message.get('Pot1')
    Test_berichten_Pot2=message.get('Pot2')
    
    if(Test_berichten_Pot1 == 232):
        print('werkt')
    if(Test_berichten_Pot2 <= 200):
        print('owjo')
    
    


    
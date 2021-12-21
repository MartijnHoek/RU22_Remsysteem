# Startup (libraries)

import can                                           # Importeert can library       (CAN)
import cantools                                      # Importeert can library       (CAN)
from can.message import Message                      # Importeert can library       (CAN)

import keyboard                                      # Importeert keyboard library  (RPi)
import time                                          # Importeert time library      (RPi)

import board                                         # Importeert board library     (adafruit)
import busio                                         # Importeert busio library     (adafruit)
import digitalio                                     # Importeert digitalio library (adafruit)
import pulseio                                       # Importeert pulseio library   (adafruit)
import adafruit_ads1x15.ads1015 as ADS               # Importeert ADS library       (adafruit)
from adafruit_ads1x15.analog_in import AnalogIn      # Importeer AnalogIn library   (adafruit)

import Remsysteem_Functies 

# Analoog / Digitaal Converter
i2c = busio.I2C(board.SCL, board.SDA)                # busio.I2C creeert een interface voor de I2C protocol
ads = ADS.ADS1015(i2c)                               # De ADS drive wordt aangegeven welke interface toegepast moet worden
chan1 = AnalogIn(ads, ADS.P0)                        # De toegepaste kanalen op de ADC worden gedefineerd
chan2 = AnalogIn(ads, ADS.P1)                        # De toegepaste kanalen op de ADC worden gedefineerd

# Motor aansturing
dir1 = digitalio.DigitalInOut(board.D26)             # Pin 26 wordt aangeduid als een digitale In-/Output
dir2 = digitalio.DigitalInOut(board.D24)             # Pin 24 wordt aangeduid als een digitale In-/Output
dir1.direction = digitalio.Direction.OUTPUT          # Pin 26 wordt als Output gedefineerd 
dir2.direction = digitalio.Direction.OUTPUT          # Pin 24 wordt als Output gedefineerd
PWM = pulseio.PWMOut(board.D12)                      # Pin 12 wordt aangeduid als een PWM output pin
           
Signalen_Remdruksensor = Remsysteem_Functies.Remdruksensor(chan1, chan2)

class Keyboard:                                      # Klasse voor het toetsenbord wordt aangemaakt 
    def __init__ (self, PWM):                        # De klasse wordt geinitialiseerd
        self.PWM =  PWM                              # De PWM wordt aangeduid
        self.block = True                            # De block parameter wordt op True gezet 
        self.display = True                          # De display parameter wordt op True gezet 
        
    def motor_uit(self):                             # De motor_uit functie wordt aangemaakt, hierin wordt de DC op 0 gezet en wordt er motor uit geprint 
        PWM.duty_cycle = 0                           # in de terminal  
        #print("Motor Uit")       
        dir1.value = True                            # De richting van de motor wordt vastgesteld als 1 = True en 2 False is de richting rechtsom 
        dir2.value = False       
        
    def motor_aan(self):                             # De motor aan functie wordt aangemaakt, hierin wordt de DC op 65535 gezet (maximale waarde) en wordt er
        PWM.duty_cycle = 65535                       # in de terminal aangegeven dat de motor geactiveerd is.
        #print("Motor Aan")        
        dir1.value = True
        dir2.value = False
        
    def Toggle_k(self):
        if keyboard.is_pressed("k"):             # Wanneer toets k ingedrukt open loop      
            if self.block == False:              # Wanneer waarde block gelijk is aan False open loop
                self.display = not self.display  # De waarde van Display wordt omgedraaid True -> False en andersom  dit is belangrijk voor de onderstaande IF loop
                self.block = True                # Waarde van Block wordt True zodat loop niet opnieuw opend
        else: 
            self.block = False                   # Block wordt terug op False gezet
        return self.display
 
eigen_keyboard = Keyboard(0)

bus = can.interface.Bus(channel='can0', bustype='socketcan_native')                           # Maakt de CAN bus aan (type bus en kanaal wordt gedefineerd)
db = cantools.db.load_file('/home/pi/Desktop/RU22_Remsysteem/FSG_Data_Logger_data_V1.1.dbc')  # Laad het .dbc file voor ontcijferen berichten
Test_berichten = db.get_message_by_name('Test_berichten')                                     # Ontcijfert de Test_berichten uit het .dbc file

class CAN:                                       # Maakt de CAN klasse aan
    def __init__ (self, Remdruk):                # De klasse wordt geinitialiseerd 
        self.Remdruk = Remdruk   

    def Remdruksensoren(self):                                                            # De data voor de remdruksensoren
        Sensor1Stand = Remsysteem_Functies.arduino_map(Signalen_Remdruksensor.chan1.voltage, 0, 3.3, 0, 255)  # De Arduino map functie voor de sensor data omgezet naar decimaal
        Sensor2Stand = Remsysteem_Functies.arduino_map(Signalen_Remdruksensor.chan2.voltage, 0, 3.3, 0, 255)  # Idem
        Test_berichten_data = Test_berichten.encode({'Pot1':Sensor1Stand, 'Pot2':Sensor2Stand}) # Er wordt aangegeven welke data bij welke aangegeven .dbc waarde hoort            
        Test_berichten_bericht=can.Message(arbitration_id=Test_berichten.frame_id, data=Test_berichten_data) # Het CAN bericht wordt opgesteld
        bus.send(Test_berichten_bericht)                                                        # Het bericht wordt over de bus verzonden

    def Ontvangen(self):                                                     # Het ontvangen en verwerken van data over de CAN bus
        message = bus.recv()                                                 # Berichten van de bus worden verbonden aan parameter message
        if message.arbitration_id == 512:                                    # Als berichten met deze arbitrage binnen komen wordt de volgende loop geopend
            message=db.decode_message(message.arbitration_id, message.data)  # Het bericht wordt omgezet naar uitleesbare data
            Test_berichten_Pot1=message.get('Pot1')                          # De data worden uitgelezen op basis van de verbonden waardes in het .dbc file
            Test_berichten_Pot2=message.get('Pot2')                          # Idem 
        
            if(Test_berichten_Pot1 == 232):        # Tijdens testfase gebruikt om te controleren hoe verkregen data verwerkt werdt                          
                print('werkt')
            if(Test_berichten_Pot2 <= 200):
                print('owjo')        
        else:
            print("Joeri's berichten")
            
CAN_bus = CAN(0)

while True:                                                   
                                                      # De klasse keyboard wordt geopend, hierin wordt de Press functie toegepast, wanneer de k toets ingedrukt    
    if eigen_keyboard.Toggle_k() :                    # wordt zal de code in deze klasse geactiveerd worden (en zal de motor in/uitgeschakeld worden) 
        eigen_keyboard.motor_uit()                    # Als Display True is opend deze loop
    else:                                             # Als Display False is opend deze loop
        eigen_keyboard.motor_aan()

    CAN_bus.Remdruksensoren()                         # De Remdruksensoren data wordt uitgezonden
    CAN_bus.Ontvangen()                               # Data vanuit de CAN bus wordt ontvangen

    #print(Signalen_Remdruksensor.meet())              # De gemeten waardes uit de remdruksensor klasse worden geprint in de terminal
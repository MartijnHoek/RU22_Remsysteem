# Startup (libraries)
import keyboard                                      # Importeert keyboard library  (RPi)
import time                                          # Importeert time library      (RPi)
import board                                         # Importeert board library     (adafruit)
import busio                                         # Importeert busio library     (adafruit)
import digitalio                                     # Importeert digitalio library (adafruit)
import pulseio                                       # Importeert pulseio library   (adafruit)
import adafruit_ads1x15.ads1015 as ADS               # Importeert ADS library       (adafruit)
from adafruit_ads1x15.analog_in import AnalogIn      # Importeer AnalogIn library   (adafruit)

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

class Remdruksensor:                                 # Klasse voor de remdruksensor wordt aangemaakt
    def __init__(self, chan1, chan2):                # De klasse wordt geinitialiseerd
        self.chan1 = chan1                           # Kanaal 1 wordt aangeduid
        self.chan2 = chan2                           # Kanaal 2 wordt aangeduid

    def meet(self):                                  # De meet klasse wordt aangemaakt, in deze klasse wordt het analoge signal omgezet naar digitaal.
        meetwaarde = round(chan1.voltage,2),round(chan2.voltage,2),\
             int(chan1.voltage/(chan1.voltage+chan2.voltage)*100), int(chan2.voltage/(chan1.voltage+chan2.voltage)*100)
        return meetwaarde

class Keyboard:                                      # Klasse voor het toetsenbord wordt aangemaakt 
    def __init__ (self, PWM):                        # De klasse wordt geinitialiseerd
        self.PWM =  PWM                              # De PWM wordt aangeduid
        self.block = True                            # De block parameter wordt op True gezet 
        self.display = True                          # De display parameter wordt op True gezet 
        
    def motor_uit(self):                             # De motor_uit functie wordt aangemaakt, hierin wordt de DC op 0 gezet en wordt er motor uit geprint 
        PWM.duty_cycle = 0                           # in de terminal  
        print("Motor Uit")       
        dir1.value = True                            # De richting van de motor wordt vastgesteld als 1 = True en 2 False is de richting rechtsom 
        dir2.value = False       
        
    def motor_aan(self):                             # De motor aan functie wordt aangemaakt, hierin wordt de DC op 65535 gezet (maximale waarde) en wordt er
        PWM.duty_cycle = 65535                       # in de terminal aangegeven dat de motor geactiveerd is.
        print("Motor Aan")        
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
            
Signalen_Remdruksensor = Remdruksensor(chan1, chan2)
   
eigen_keyboard = Keyboard(0)
   
while True:                                                   
                                                      # De klasse keyboard wordt geopend, hierin wordt de Press functie toegepast, wanneer de k toets ingedrukt    
    if eigen_keyboard.Toggle_k() :                    # wordt zal de code in deze klasse geactiveerd worden (en zal de motor in/uitgeschakeld worden) 
        eigen_keyboard.motor_uit()                    # Als Display True is opend deze loop
    else:                                             # Als Display False is opend deze loop
        eigen_keyboard.motor_aan()

    print(Signalen_Remdruksensor.meet())              # De gemeten waardes uit de remdruksensor klasse worden geprint in de terminal

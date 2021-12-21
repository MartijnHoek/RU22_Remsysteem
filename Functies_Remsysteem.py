import board                                         # Importeert board library     (adafruit)
import keyboard                                      # Importeert keyboard library  (RPi)
import digitalio                                     # Importeert digitalio library (adafruit)

# Motor aansturing
dir1 = digitalio.DigitalInOut(board.D26)             # Pin 26 wordt aangeduid als een digitale In-/Output
dir2 = digitalio.DigitalInOut(board.D24)             # Pin 24 wordt aangeduid als een digitale In-/Output
dir1.direction = digitalio.Direction.OUTPUT          # Pin 26 wordt als Output gedefineerd 
dir2.direction = digitalio.Direction.OUTPUT          # Pin 24 wordt als Output gedefineerd

# Arduino Map Functie

def arduino_map(x, in_min, in_max, out_min, out_max):#Maakt de Arduino map() functie na voor het verwerken van analoge signalen                          
    return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min

# Keyboard functies

class Keyboard:                                      # Klasse voor het toetsenbord wordt aangemaakt 
    def __init__ (self, PWM):                        # De klasse wordt geinitialiseerd
        self.PWM =  PWM                              # De PWM wordt aangeduid
        self.block = True                            # De block parameter wordt op True gezet 
        self.display = True                          # De display parameter wordt op True gezet 
        
    def motor_uit(self,PWM):                             # De motor_uit functie wordt aangemaakt, hierin wordt de DC op 0 gezet en wordt er motor uit geprint 
        PWM.duty_cycle = 0                           # in de terminal  
        #print("Motor Uit")       
        dir1.value = True                            # De richting van de motor wordt vastgesteld als 1 = True en 2 False is de richting rechtsom 
        dir2.value = False       
        
    def motor_aan(self,PWM):                             # De motor aan functie wordt aangemaakt, hierin wordt de DC op 65535 gezet (maximale waarde) en wordt er
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

eigen_keyboard =Keyboard(0)
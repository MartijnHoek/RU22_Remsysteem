# Startup 
import RPi.GPIO as GPIO         # Importeert RPi.GPIO library en hernoemd naar GPIO
import keyboard                 # Importeert keyboard library

#display = True

GPIO.setwarnings(False)                        # Zet GPIO waarschuwingen uit
GPIO.setmode(GPIO.BOARD)                       # Stelt de GPIO layout in (BOARD gekozen)
GPIO.setup(12, GPIO.OUT, initial=GPIO.LOW)     # GPIO instellingen voor het LED, standaard op LOW gezet
GPIO.setup(32, GPIO.OUT)		               # GPIO instellingen voor PWM pin
GPIO.setup(37, GPIO.OUT)		               # GPIO instellingen voor Directie 
p1 = GPIO.PWM(32, 100)			               # PWM instellingen waarbij (Kanaal/pin, frequentie)

class Keyboard:
    def __init__ (self, PWM):
        self.PWM =  PWM
        self.block = True
        self.display = True
        
    def motor_uit(self):
        GPIO.output(37, GPIO.HIGH)
        p1.start(1)
        print("Motor Uit")
        
    def motor_aan(self):
        GPIO.output(37, GPIO.HIGH)
        p1.start(100)
        print("Motor Aan")
        
    def Press(self):
        if self.block == False:              # Wanneer waarde block gelijk is aan False open loop
            print("Werkt")
            self.display = not self.display       # De waarde van Display wordt omgedraaid True -> False en andersom  dit is belangrijk voor de onderstaande IF loop
            self.block = True                # Waarde van Block wordt True zodat loop niet opnieuw opend
   
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
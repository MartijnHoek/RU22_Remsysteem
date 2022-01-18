import RPi.GPIO as GPIO

class DOGA:
    
    def __init__(self,doga_pwm,doga_dir,freq):
        
        self.doga_PWM = doga_pwm
        self.doga_dir = doga_dir
        self.freq = freq

        GPIO.setwarnings(False)
        #GPIO.setmode(GPIO.BOARD)
        GPIO.setup(self.doga_dir,GPIO.OUT)                                               # Cytron MD20A DIR 
        GPIO.setup(self.doga_PWM,GPIO.OUT)                                               # Cytron MD20A PWM

        self.doga_pwm = GPIO.PWM(self.doga_PWM, self.freq)
        self.doga_pwm.start(0)

    def motor_aansturen(self,pwm):
        self.pwm = pwm
        
        if self.pwm >= 0:
            GPIO.output(self.doga_dir,True)
            self.doga_pwm.ChangeDutyCycle(self.pwm)
                
        elif self.pwm < 0:
            GPIO.output(self.doga_dir,False)
            self.doga_pwm.ChangeDutyCycle(abs(self.pwm))
            
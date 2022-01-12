# Startup (libraries)
import pulseio               # Importeert de library voor de motor aansturing (PWM signalen)
import board                 # Importeert de library voor de motor aansturing (pin aanduiding)

import Functies_Remsysteem   # Importeert de overige functies voor het remsysteem script
import CANbus_Remsysteem     # Importeert de CAN bus library waarin de CAN berichten van het remsysteem verwerkt worden

import os                    # Importeert Operating System library (OS)

os.system("sudo /sbin/ip link set can0 up type can bitrate 500000") # Instellingen voor setup CAN-bus
eigen_keyboard = Functies_Remsysteem.Keyboard()
CAN_bus = CANbus_Remsysteem.CAN()   

while True:                                                    
   
    if eigen_keyboard.Toggle_k() :                            # wordt zal de code in deze klasse geactiveerd worden (en zal de motor in/uitgeschakeld worden) 
        eigen_keyboard.motor_uit(pulseio.PWMOut(board.D12))   # Als Display True is opend deze loop
    else:                                                     # Als Display False is opend deze loop
        eigen_keyboard.motor_aan(pulseio.PWMOut(board.D12))

    CAN_bus.Verzenden()                                   # De Remdruksensoren data wordt uitgezonden
    CAN_bus.Ontvangen()                                   # Data vanuit de CAN bus wordt ontvangen
  
    if CAN_bus.Service_Mode == 1 or CAN_bus.Service_Mode == 3:
        #print('Service_Mode 1 of 3')
        # Geen Actie
        pass
    
    elif CAN_bus.Service_Mode == 2:
        #print('Service_Mode 2')
        # Pedaal stand naar 0 %
        pass
    
    if CAN_bus.Systeem_Mode == 1 or CAN_bus.Systeem_Mode == 4:
        #print('Systeem_Mode 1 of 4')
        # Pedaalstand naar 0
        pass

    elif CAN_bus.Systeem_Mode == 2 or CAN_bus.Systeem_Mode == 5:
        #print('Systeem_Mode 2 of 5')
        # Pedaalstand naar 100
        pass
    
    elif CAN_bus.Systeem_Mode == 3:
        #print('Systeem_Mode 3')
        # Pedaalstand Dynamisch
        pass
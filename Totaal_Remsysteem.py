# Startup (libraries)
import pulseio               # Importeert de library voor de motor aansturing (PWM signalen)
import board                 # Importeert de library voor de motor aansturing (pin aanduiding)

import Functies_Remsysteem   # Importeert de overige functies voor het remsysteem script
import CANbus_Remsysteem     # Importeert de CAN bus library waarin de CAN berichten van het remsysteem verwerkt worden

while True:                                                   
                                                                                  # De klasse keyboard wordt geopend, hierin wordt de Press functie toegepast, wanneer de k toets ingedrukt    
    if Functies_Remsysteem.eigen_keyboard.Toggle_k() :                            # wordt zal de code in deze klasse geactiveerd worden (en zal de motor in/uitgeschakeld worden) 
        Functies_Remsysteem.eigen_keyboard.motor_uit(pulseio.PWMOut(board.D12))   # Als Display True is opend deze loop
    else:                                                                         # Als Display False is opend deze loop
        Functies_Remsysteem.eigen_keyboard.motor_aan(pulseio.PWMOut(board.D12))

    CANbus_Remsysteem.CAN_bus.Remdruksensoren()                                   # De Remdruksensoren data wordt uitgezonden
    CANbus_Remsysteem.CAN_bus.Ontvangen()                                         # Data vanuit de CAN bus wordt ontvangen
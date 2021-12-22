#sudo /sbin/ip link set can0 up type can bitrate 500000 # Instellingen voor setup CAN-bus

# Startup (libraries)
import cantools                     # Importeert can library      (CAN)
import can                          # Importeert can library      (CAN)
from can.message import Message     # Importeert can library      (CAN)

bus = can.interface.Bus(channel='can0', bustype='socketcan_native')                           # Maakt de CAN bus aan (type bus en kanaal wordt gedefineerd)
db = cantools.db.load_file('/home/pi/Desktop/RU22_Remsysteem/FSG_Data_Logger_data_V1.1.dbc')  # Laad het .dbc file voor ontcijferen berichten
Test_berichten = db.get_message_by_name('Test_berichten')                                     # Ontcijfert de Test_berichten uit het .dbc file
Aansturing_Remsysteem = db.get_message_by_name('Aansturing_Remsysteem')                       # Ontcijfert de Aansturing_Remsysteem berichten uit het .dbc file

def arduino_map(x, in_min, in_max, out_min, out_max): # De meet klasse wordt aangemaakt, in deze klasse wordt het analoge signal omgezet naar digitaal.
    return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min

while True:
    
    # Test berichten bericht
    
    Sensor1Stand = arduino_map(3, 0, 3.3, 0, 255)     # Een sensor waarde met voltage naar decimale omzet wordt aangemaakt
    Sensor2Stand = arduino_map(3, 0, 3.3, 0, 255)     # Een sensor waarde met voltage naar decimale omzet wordt aangemaakt

    Test_berichten_data = Test_berichten.encode({'Pot1':Sensor1Stand, 'Pot2':Sensor2Stand})   # Er wordt aangegeven welke data bij welke aangegeven .dbc waarde hoort   
    Test_berichten_bericht=can.Message(arbitration_id = Test_berichten.frame_id, data = Test_berichten_data)    # Het CAN bericht wordt opgesteld
    bus.send(Test_berichten_bericht)                                                                            # Het bericht wordt over de bus verzonden
    
    # Aansturing Remsysteem bericht
    
    Actual_snelheid = 70              # Voertuigsnelheid in km/h
    Target_snelheid = 50              # Gewenste voertuigsnelheid in km/h
    Systeem_Mode = 1                  # Systeem modus van het autonome systeem 0 = off, 1 = ready, 2 = driving, 3 = emergency brake, 4 = finish
    Service_Mode = 3                  # Service modus van het remsysteem 1 = disengaged, 2 = engaged, 3 = available
    Stuurhoek = 45                    # Stuurhoek 
    
    # Zelfde proces als Test_berichten (er wordt een bericht aangemaakt en verzonden)
    Aansturing_Remsysteem_data = Aansturing_Remsysteem.encode({'Actual_snelheid':Actual_snelheid, 'Target_snelheid': Target_snelheid, 'Systeem_Mode': Systeem_Mode, 'Service_Mode': Service_Mode, 'Stuurhoek':Stuurhoek})
    Aansturing_Remsysteem_bericht = can.Message(arbitration_id = Aansturing_Remsysteem.frame_id, data = Aansturing_Remsysteem_data)
    bus.send(Aansturing_Remsysteem_bericht)
      
    message = bus.recv()                                             # Berichten van de bus worden verbonden aan parameter 'message'
    message=db.decode_message(message.arbitration_id, message.data)  # De berichten worden gedecodeerd aan de hand van de dbc file
    Test_berichten_Pot1=message.get('Pot1')                          # Met behulp van het dbc file worden specifieke waardes uit de data gehaald
    Test_berichten_Pot2=message.get('Pot2')                          # Idem
    
    print(Test_berichten_Pot1)                                       # Ontvangen data wordt geprint
    print(Test_berichten_Pot2)
    
    if(Test_berichten_Pot1 == 232):                                  # Een loopje wordt geopend om te testen of de data verwerkt wordt door het script
        print('werkt')
    if(Test_berichten_Pot2 <= 200):
        print('owjo') 

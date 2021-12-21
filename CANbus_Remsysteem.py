import can                                           # Importeert can library       (CAN)
import cantools                                      # Importeert can library       (CAN)
from can.message import Message                      # Importeert can library       (CAN)

import Functies_Remsysteem
import ADC_Remsysteem

bus = can.interface.Bus(channel='can0', bustype='socketcan_native')                           # Maakt de CAN bus aan (type bus en kanaal wordt gedefineerd)
db = cantools.db.load_file('/home/pi/Desktop/RU22_Remsysteem/FSG_Data_Logger_data_V1.1.dbc')  # Laad het .dbc file voor ontcijferen berichten
Test_berichten = db.get_message_by_name('Test_berichten')                                     # Ontcijfert de Test_berichten uit het .dbc file

class CAN:                                       # Maakt de CAN klasse aan
    def __init__ (self, Remdruk):                # De klasse wordt geinitialiseerd 
        self.Remdruk = Remdruk   

    def Remdruksensoren(self):                                                            # De data voor de remdruksensoren
        Sensor1Stand = Functies_Remsysteem.arduino_map(ADC_Remsysteem.Signalen_Remdruksensor.chan1.voltage, 0, 3.3, 0, 255)  # De Arduino map functie voor de sensor data omgezet naar decimaal
        Sensor2Stand = Functies_Remsysteem.arduino_map(ADC_Remsysteem.Signalen_Remdruksensor.chan2.voltage, 0, 3.3, 0, 255)  # Idem
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
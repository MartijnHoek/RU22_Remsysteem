import can                                           # Importeert can library       (CAN)
import cantools                                      # Importeert can library       (CAN)
from can.message import Message                      # Importeert can library       (CAN)

import Functies_Remsysteem                           # Importeert de overige functies voor het remsysteem script
import ADC_Remsysteem                                # Importeert de functies voor de ADC 

bus = can.interface.Bus(channel='can0', bustype='socketcan_native')                           # Maakt de CAN bus aan (type bus en kanaal wordt gedefineerd)
db = cantools.db.load_file('/home/pi/Desktop/RU22_Remsysteem/FSG_Data_Logger_data_V1.1.dbc')  # Laad het .dbc file voor ontcijferen berichten
Test_berichten = db.get_message_by_name('Test_berichten')                                     # Ontcijfert de Test_berichten uit het .dbc file
Aansturing_Remsysteem = db.get_message_by_name('Aansturing_Remsysteem')                       # Ontcijfert de Aansturing_Remsysteem berichten uit het .dbc file

class CAN:                                                                                # Maakt de CAN klasse aan  

    def Remdruksensoren(self):                                                            # De data voor de remdruksensoren
        Test_berichten = db.get_message_by_name('Test_berichten')                         # Ontcijfert de Test_berichten uit het .dbc file
        Sensor1Stand = Functies_Remsysteem.arduino_map(ADC_Remsysteem.Signalen_Remdruksensor.chan1.voltage, 0, 3.3, 0, 255)  # De Arduino map functie voor de sensor data omgezet naar decimaal
        Sensor2Stand = Functies_Remsysteem.arduino_map(ADC_Remsysteem.Signalen_Remdruksensor.chan2.voltage, 0, 3.3, 0, 255)  # Idem
        Test_berichten_data = Test_berichten.encode({'Pot1':Sensor1Stand, 'Pot2':Sensor2Stand}) # Er wordt aangegeven welke data bij welke aangegeven .dbc waarde hoort            
        Test_berichten_bericht=can.Message(arbitration_id=Test_berichten.frame_id, data=Test_berichten_data) # Het CAN bericht wordt opgesteld
        bus.send(Test_berichten_bericht)                                                  # Het bericht wordt over de bus verzonden

    def Ontvangen(self):                                                         # Het ontvangen en verwerken van data over de CAN bus
        message = bus.recv()                                                     # Berichten van de bus worden verbonden aan parameter message
        if message.arbitration_id == 512:                                        # Leest het bericht uit als deze een ID heeft van 512
            message512 = db.decode_message(message.arbitration_id, message.data) # Ontcijfert de data afkomstig uit bericht 'message'
            Test_berichten_Pot1=message512.get('Pot1')                           # De data worden uitgelezen op basis van de verbonden waardes in het .dbc file
            Test_berichten_Pot2=message512.get('Pot2')                           # Idem
            
            #print(Test_berichten_Pot1, Test_berichten_Pot2) 
            print(message512)
        
         
        elif message.arbitration_id == 514:                                      # Leest het bericht uit als deze een ID heeft van 514
            message514 = db.decode_message(message.arbitration_id, message.data) # Ontcijfert de data afkomstig uit bericht 'message'
            Actual_snelheid = message514.get('Actual_snelheid')                  # De data wordt uitgelezen op basis van de verbonden waardes in het .dbc file
            Target_snelheid = message514.get('Target_snelheid')                  # Idem voor onderstaand
            Systeem_Mode = message514.get('Systeem_Mode')
            Service_Mode = message514.get('Service_Mode')
            Stuurhoek = message514.get('Stuurhoek')
            
            #print(Actual_snelheid, Target_snelheid, Systeem_Mode, Service_Mode, Stuurhoek) 
            print(message514)
            
        else:                                                                    # Overige berichten worden niet gelezen, momenteel aangegeven met print functie
            print("Overige berichten")
            
CAN_bus = CAN()            
import can                                           # Importeert can library       (CAN)
import cantools                                      # Importeert can library       (CAN)
from can.message import Message                      # Importeert can library       (CAN)

import Functies_Remsysteem                           # Importeert de overige functies voor het remsysteem script
import ADC_Remsysteem                                # Importeert de functies voor de ADC 

Over_Travel_switch = Functies_Remsysteem.Over_travel_switch()

class CAN:                                                                                # Maakt de CAN klasse aan
    
    def __init__(self):
        self.bus = can.interface.Bus(channel='can0', bustype='socketcan_native')                           # Maakt de CAN bus aan (type bus en kanaal wordt gedefineerd)
        self.db = cantools.db.load_file('/home/pi/Desktop/RU22_Remsysteem/FSG_Data_Logger_data_V1.1.dbc')  # Laad het .dbc file voor ontcijferen berichten
        self.Verzending_Remsysteem = self.db.get_message_by_name('Verzending_Remsysteem')                  # Ontcijfert de Verzending_Remsysteem uit het .dbc file
        self.Aansturing_Remsysteem = self.db.get_message_by_name('Aansturing_Remsysteem')                  # Ontcijfert de Aansturing_Remsysteem berichten uit het .dbc file            
       
    def Verzenden(self):                                                                       # De data voor de remdruksensoren    
        Verzenden_Remsysteem = self.db.get_message_by_name('Verzending_Remsysteem')                  # Ontcijfert de Test_berichten uit het .dbc file
        Verzenden_Remsysteem_CR = 45                                                           # Parameter voor de data Current_Rempedaal wordt aangemaakt
        Over_Travel_switch.Positie_meting() 
        Verzenden_Remsysteem_OVS = Over_Travel_switch.Schakelaarstand # Parameter voor de data Overtravel_switch wordt aangemaakt
        print(Verzenden_Remsysteem_OVS)
        Verzenden_Remsysteem_data = Verzenden_Remsysteem.encode({'Current_Rempedaal':Verzenden_Remsysteem_CR, 'Overtravel_switch':Verzenden_Remsysteem_OVS}) # Er wordt aangegeven welke data bij welke aangegeven .dbc waarde hoort            
        Verzenden_Remsysteem_bericht=can.Message(arbitration_id=Verzenden_Remsysteem.frame_id, data=Verzenden_Remsysteem_data) # Het CAN bericht wordt opgesteld
        self.bus.send(Verzenden_Remsysteem_bericht)                                            # Het bericht wordt over de bus verzonden

    def Ontvangen(self):                                                         # Het ontvangen en verwerken van data over de CAN bus
        message = self.bus.recv()                                                     # Berichten van de bus worden verbonden aan parameter message
        
        if message.arbitration_id == 512:                                      # Leest het bericht uit als deze een ID heeft van 514
             message514 = self.db.decode_message(message.arbitration_id, message.data) # Ontcijfert de data afkomstig uit bericht 'message'                         
             Target_Rempedaal = message514.get('Target_Rempedaal')                  # De data wordt uitgelezen op basis van de verbonden waardes in het .dbc file
             Systeem_Mode = message514.get('Systeem_Mode')
             Service_Mode = message514.get('Service_Mode')
                           
             print(Target_Rempedaal, Systeem_Mode, Service_Mode) 
             #print(message514)
            
#         elif message.arbitration_id == 514:                                      # Leest het bericht uit als deze een ID heeft van 514
#             message514 = self.db.decode_message(message.arbitration_id, message.data) # Ontcijfert de data afkomstig uit bericht 'message'                         
#             Target_Rempedaal = message514.get('Target_Rempedaal')                  # De data wordt uitgelezen op basis van de verbonden waardes in het .dbc file
#             Systeem_Mode = message514.get('Systeem_Mode')
#             Service_Mode = message514.get('Service_Mode')
#                           
#             print(Target_Rempedaal, Systeem_Mode, Service_Mode) 
#             #print(message514)      
                           
        else:                                                                    # Overige berichten worden niet gelezen, momenteel aangegeven met print functie
            print("Overige berichten")
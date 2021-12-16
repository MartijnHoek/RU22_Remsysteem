#sudo /sbin/ip link set can0 up type can bitrate 500000 # Instellingen voor setup CAN-bus

# Startup (libraries)
import cantools
import can
from can.message import Message

bus = can.interface.Bus(channel='can0', bustype='socketcan_native')
db = cantools.db.load_file('/home/pi/RU22_Remsysteem/Test_DBC_Files.dbc')
Test_berichten = db.get_message_by_name('Test_berichten')

def arduino_map(x, in_min, in_max, out_min, out_max):
    return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min

while True:
    
    Sensor1Stand = arduino_map(3, 0, 3.3, 0, 255)
    Sensor2Stand = arduino_map(3, 0, 3.3, 0, 255)

    Test_berichten_data = Test_berichten.encode({'Pot1':Sensor1Stand, 'Pot2':Sensor2Stand})
    Test_berichten_bericht=can.Message(arbitration_id=Test_berichten.frame_id, data=Test_berichten_data)
    bus.send(Test_berichten_bericht)
    
    message = bus.recv()
    message=db.decode_message(message.arbitration_id, message.data) 
    Test_berichten_Pot1=message.get('Pot1')
    Test_berichten_Pot2=message.get('Pot2')
    
    print(Test_berichten_Pot1)
    print(Test_berichten_Pot2)
    
    if(Test_berichten_Pot1 == 232):
        print('werkt')
    if(Test_berichten_Pot2 <= 200):
        print('owjo') 
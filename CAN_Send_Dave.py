#sudo /sbin/ip link set can0 up type can bitrate 500000 # Instellingen voor setup CAN-bus

# Startup (libraries)
import cantools
import can
from can.message import Message

db = cantools.db.load_file('/home/pi/RU22_Remsysteem/Test_DBC_Files.dbc')
msg = db.get_message_by_name('Test_berichten')
bus = can.interface.Bus(channel='can0', bustype='socketcan_native')

def arduino_map(x, in_min, in_max, out_min, out_max):
    return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min

while True:
    
    Sensor1Stand = arduino_map(3, 0, 3.3, 0, 255)
    Sensor2Stand = arduino_map(3, 0, 3.3, 0, 255)

    msg_data = msg.encode({'Pot1':Sensor1Stand, 'Pot2':Sensor2Stand})
    bericht=can.Message(arbitration_id=msg.frame_id, data=msg_data)
    bus.send(bericht)
    
    message = bus.recv()
    print(db.decode_message(message.arbitration_id, message.data)) 
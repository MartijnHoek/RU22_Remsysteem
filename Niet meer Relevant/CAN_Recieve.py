#sudo /sbin/ip link set can0 up type can bitrate 500000

import can
import cantools
from can.message import Message
import time

db = cantools.db.load_file('/home/pi/RU22_Remsysteem/Test_DBC_Files.dbc')

bus = can.interface.Bus(channel='can0', bustype='socketcan_native')

while True:
    message = bus.recv()
    print(db.decode_message(message.arbitration_id, message.data))
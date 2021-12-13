#sudo /sbin/ip link set can0 up type can bitrate 500000 # Instellingen voor setup CAN-bus

import can
import time

bus = can.interface.Bus(channel='can0', bustype='socketcan_native')
#msg = can.Message(arbitration_id=0x502, data=[6, 17], extended_id=False)
#bus.send(msg)

#notifier = can.Notifier(bus, [can.Printer()])

while True:
    
    data = int(input("Vul een decimale waarde in (min:0 max:255):  "))
    msg = can.Message(arbitration_id=0x502, data=[data], extended_id=False)
    bus.send(msg)
    time.sleep(1)

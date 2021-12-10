import can
import time

bus = can.interface.Bus(channel='can0', bustype='socketcan_native')
#msg = can.Message(arbitration_id=0x502, data=[6, 17], extended_id=False)
#bus.send(msg)

#notifier = can.Notifier(bus, [can.Printer()])

while True:
    notifier = can.Notifier(bus, [can.Printer()])
    time.sleep(1000)
    
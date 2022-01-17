import board
import digitalio                                     # Importeert digitalio library (adafruit)

direction_pin = digitalio.DigitalInOut(board.D27)
direction_pin.pull = digitalio.Pull.UP

step_pin = digitalio.DigitalInOut(board.D23)
step_pin.pull = digitalio.Pull.UP

previous_value = True

teller = 0

helpe = 0 

daf = 0

while True:
# #     
#     if step_pin.value == True:
#         teller=teller +1 
#         print('Teller',teller)
#    
#     if step_pin.value == False:
#         helpe=helpe+1
#         print('Helpe', helpe)

    if step_pin.value == True and direction_pin.value == True:
        daf = daf +1
        print(daf)
        
#     
#     if previous_value != step_pin.value:
#         if step_pin.value == False:
#             if direction_pin.value == False:
#                 print("Turned Left")
#             else:
#                 print("Turned Right")
#         previous_value = step_pin.value
    
    
    #print(direction_pin.value)
    #print(step_pin.value)
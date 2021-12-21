# Bestand waaruit diverse functies opgeroepen kunnen worden voor het Drive By Wire Remsysteem van de RU22

# Arduino Map Functie

def arduino_map(x, in_min, in_max, out_min, out_max):#Maakt de Arduino map() functie na voor het verwerken van analoge signalen                          
    return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min

# Remdruksensor meetwaardes

class Remdruksensor:                                 # Klasse voor de remdruksensor wordt aangemaakt
    def __init__(self, chan1, chan2):                # De klasse wordt geinitialiseerd
        self.chan1 = chan1                           # Kanaal 1 wordt aangeduid
        self.chan2 = chan2                           # Kanaal 2 wordt aangeduid
        
    def meet(self):                                  # De meet klasse wordt aangemaakt, in deze klasse wordt het analoge signal omgezet naar digitaal.
        meetwaarde = round(chan1.voltage,2),round(chan2.voltage,2),\
             int(chan1.voltage/(chan1.voltage+chan2.voltage)*100), int(chan2.voltage/(chan1.voltage+chan2.voltage)*100)
        return meetwaarde
    
# Keyboard functies


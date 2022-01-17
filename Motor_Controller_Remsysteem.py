from encoder import Encoder

class Hall:
    
    def __init__(self,A,B):
        self.A = A
        self.B = B
        self.angle = 0
        self.e1 = Encoder(self.A,self.B)

    def Hoek_meting(self):
        self.angle = self.e1.getValue() * (360/972)
        print(self.angle)
        return self.angle


from simple_pid import PID

class PIDC:
    
    def __init__(self,p,i,d,ll,ul):
        self.p = p
        self.i = i
        self.d = d
        self.ll = ll
        self.ul = ul
        self.sp = 0
        self.pwm = 0
        
    def spcalc(self,gw):
        self.gw = gw
     
        self.sp = float(self.gw) 
     
        self.pid = PID(self.p,self.i,self.d,setpoint = self.sp)
        self.pid.output_limits = (self.ll,self.ul)
        #print(self.sp)
        return self.sp
    
    def pidexc(self,a):
        self.a = a
        self.pwm = self.pid(a)
        #print(self.a,self.pwm)
        return self.a, self.pwm

    def get_pwm(self):
        return self.pwm

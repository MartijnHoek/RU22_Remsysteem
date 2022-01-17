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
        self.sp = ((360/972) * round((float(self.gw)/(32.78/135))/(360/972)))

        if self.sp > 134.82:
            self.sp = ((360/972) * round((32.78)/(32.78/135)/(360/972)))
        
        self.pid = PID(self.p,self.i,self.d,setpoint = self.sp)
        self.pid.output_limits = (self.ll,self.ul)
        print(self.sp)
        return self.sp
    
    def pidexc(self,a):
        self.a = a
        self.pwm = self.pid(a)
        print(self.a,self.pwm)
        return self.a, self.pwm

    def get_pwm(self):
        return self.pwm

from Raspi_MotorHAT import Raspi_MotorHAT

class HatControler():
    def __init__(self, mh = Raspi_MotorHAT(addr=0x70)):
        # seting I2C addres
        self.mh = mh
        # setinge default motors
        self.b_left = mh.getMotor(1)
        self.b_right = mh.getMotor(2)
        self.f_left = mh.getMotor(3)
        self.f_right = mh.getMotor(4)
        # setinge default speed as 0
        self.b_left.setSpeed(0)
        self.b_right.setSpeed(0)
        self.f_left.setSpeed(0)
        self.f_right.setSpeed(0)

        self.temp_speed = 0
        self.direction = "STOP"

    def run(self, speed=0.5, turn = 0.0, verical = 0.0):
        if speed == 0:
            self.stop()
            self.direction = "STOP"
            self.temp_speed = round(speed*100,2)
            return
    
        self.temp_speed = round(speed*100,2)

        self.l_polarity = Raspi_MotorHAT.FORWARD
        self.r_polarity = Raspi_MotorHAT.FORWARD
        #in Raspi_MotorHAT value of 255 is 100% motor power
        #turn defain move direction. 0 is forward, 1 is right and -1 is left
        speed = round(speed * 255)
        turn = round(turn * speed)
        #print(f"speed: {speed}")
        #print(f"turn: {turn}")
        l_speed = speed + turn
        r_speed = speed - turn
        #print(f"l: {l_speed}")
        #print(f"r: {r_speed}")

        if l_speed>255: l_speed = 255
        elif l_speed<-255: l_speed = -255
        if r_speed>255: r_speed = 255
        elif r_speed<-255: r_speed = -255

        self.b_left.setSpeed(abs(l_speed))
        self.b_right.setSpeed(abs(r_speed))
        self.f_left.setSpeed(abs(l_speed))
        self.f_right.setSpeed(abs(r_speed))

        if l_speed>0: self.l_polarity = Raspi_MotorHAT.FORWARD
        else: self.l_polarity = Raspi_MotorHAT.BACKWARD
        if r_speed>0: self.r_polarity = Raspi_MotorHAT.FORWARD
        else: self.r_polarity = Raspi_MotorHAT.BACKWARD
        if verical == 0:
            if turn < 0: self.direction = " Skręt w lewo"
            elif turn > 0: self.direction = " Skręt w prawo"
            else: self.direction = "Jazda prosto"
            
            self.b_left.run(self.l_polarity)
            self.b_right.run(self.r_polarity)
            self.f_left.run(self.l_polarity)
            self.f_right.run(self.r_polarity)
        elif verical > 0:
            self.direction = "Wertykalnie w Prawo"
            self.b_left.run(Raspi_MotorHAT.FORWARD)
            self.b_right.run(Raspi_MotorHAT.BACKWARD)
            self.f_left.run(Raspi_MotorHAT.BACKWARD)
            self.f_right.run(Raspi_MotorHAT.FORWARD)
        else:
            self.direction = "Wertykalnie w Lewo"
            self.b_left.run(Raspi_MotorHAT.BACKWARD)
            self.b_right.run(Raspi_MotorHAT.FORWARD)
            self.f_left.run(Raspi_MotorHAT.FORWARD)
            self.f_right.run(Raspi_MotorHAT.BACKWARD)


    def stop(self):
        self.b_left.setSpeed(0)
        self.b_right.setSpeed(0)
        self.f_left.setSpeed(0)
        self.f_right.setSpeed(0)

    def get_speed(self):
        return self.speed
    def get_direction(self):
        return self.direction
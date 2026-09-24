import pygame
from threading import Thread
from HatControl import HatControler
from DataCollector import DataCollector
import time
jeepMotor = HatControler()
global collector 
record = 0 #Glabal recording stage virable

class JoyControl():
    def __init__(self):
        self.speed = 0 #Glabal speed variable
        self.r_angle = 0 #Glabal rotation variable
        self.v_move = 0.0
        self.engineOff = False
        self.restrictedSpeed = False
        #Initializing the pad and creating a global variable to hold its object
        pygame.joystick.init()
        self.joystick = [pygame.joystick.Joystick(x) for x in range(pygame.joystick.get_count())]
        pygame.init()
        self.contorler = pygame.joystick.Joystick(0)

        self.clock = pygame.time.Clock() #Clock variable
       
    def EventListener(self):
        global record
        global collector
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    break
                if event.type == pygame.JOYAXISMOTION:
                    #Variables responsible for vertical movement, turning the vehicle, and accelerating
                    vertical_movement = self.contorler.get_axis(2) # stick on the left
                    turn_control = self.contorler.get_axis(0) # stick on the right
                    acceleration = self.contorler.get_axis(4) # Trigger on the right

                    if acceleration:
                        #print(acceleration)
                        if acceleration < 0: self.speed = 0
                        else: self.speed = round(acceleration,2)#Locked speed for easier data collection
                    if turn_control:
                        #turn_control = round(turn_control,2)
                        self.r_angle = -turn_control
                    else:
                        self.r_angle = 0
                    if vertical_movement:
                        self.v_move = round(vertical_movement,2)
                        self.v_move = -self.v_move
                    else:
                        self.v_move = 0
                    
                    if self.engineOff:
                        jeepMotor.run(0,self.r_angle,self.v_move)
                    elif self.restrictedSpeed and self.speed > 0:
                        jeepMotor.run(0.17,self.r_angle,self.v_move)
                    else:
                        jeepMotor.run(self.speed,self.r_angle,self.v_move)
                # Button responsible for starting data collection
                if event.type == pygame.JOYBUTTONDOWN:
                    if self.contorler.get_button(0):
                        if record == 1:
                            record = 2
                        elif record == 0:
                            #print("test")
                            collector = DataCollector(1)
                            Thread(target=self.start_collecting,args=()).start()
                            #self.start_collecting()
                    if self.contorler.get_button(1):
                        if record == 1:
                            record = 2
                        elif record == 0:
                            #print("test")
                            collector = DataCollector(2)
                            Thread(target=self.start_collecting,args=()).start()
                            #self.start_collecting()
                    if self.contorler.get_button(3):
                        if record == 1:
                            record = 2
                        elif record == 0:
                            #print("test")
                            collector = DataCollector(3)
                            Thread(target=self.start_collecting,args=()).start()
                            #self.start_collecting()
            self.clock.tick(100)

    """ Button operation test
    def test(self):
        global record
        while True:
            if record == 0:
                print ("0 ->")
                print (record)
                record = 1
                time.sleep(1)
            if record == 1:
                print ("1 ->")
                print (record)
                time.sleep(1)
            if record == 2:
                print ("2 -> ")
                print (record)
                time.sleep(1)
                record = 0
                break"""
    
    def start_collecting(self):
        global record
        while True:
            if record == 0:
                print("Rocording started......")
                record = 1
                time.sleep(0.1)
            if record == 1:
                collector.save_IMG(round(self.r_angle,2),self.speed,self.v_move)
                time.sleep(0.1)
            elif record == 2:
                collector.create_log_file()
                time.sleep(0.1)
                record = 0
                break
    
    
    def getRotation(self):
        return self.r_angle
    
    def getSpeed(self):
        return self.speed
    
    def getDirection(self):
        return jeepMotor.get_direction()
    
    def toggleEngine(self):
        self.engineOff = not self.engineOff
    
    def toggleRestrictedSpeed(self):
        self.restrictedSpeed = not self.restrictedSpeed
    
    def getRecord(self):
        global record
        if record == 0:
            return "Żadne dane nie są przetwarzane"
        elif record == 1:
            return "Trwa zbieranie danych"
        elif record == 2:
            return "Generowanie pliku log.csv"
        else:
            return "Błąd danych"

if __name__ == '__main__':
    ct = JoyControl()
    ct.EventListener()   
    print("started") 




rotation = 0.0
t_speed = 0.0


#Old function version
"""def run():
    global speed, rotation, t_speed
    speed = 0
    pygame.joystick.init()
    joystick = [pygame.joystick.Joystick(x) for x in range(pygame.joystick.get_count())]
    print(joystick)

    pygame.init()
    clock = pygame.time.Clock()


    contorler = pygame.joystick.Joystick(0)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                break
            if event.type == pygame.JOYAXISMOTION:
                vertical = contorler.get_axis(2)
                leftRight = contorler.get_axis(0)
                if contorler.get_axis(4):
                    #print(contorler.get_axis(4))
                    if contorler.get_axis(4) < 0: speed = 0
                    else: speed = contorler.get_axis(4)
                    t_speed = speed
                if leftRight:
                    jeepMotor.run(speed,round(leftRight,2))
                    rotation = round(leftRight,2)
                if vertical:
                    vertical = round(vertical,2)
                    jeepMotor.run(speed,0.0,vertical)
            if event.type == pygame.JOYBUTTONDOWN:
                if contorler.get_button(0):
                    print("button")
                    #Camera.capture_file()
        clock.tick(100)"""
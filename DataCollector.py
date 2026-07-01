"""
- This module is responsibile for data colection to fature learning. 
"""

import pandas as pd
import os
from datetime import datetime
import Camera

class DataCollector():
    def __init__(self,ver):
        self.folder_counter = 0
        self.img_list = []
        self.rotation_angle_list = []
        self.speed_list = []
        self.v_list = []
        self.version = ver
        self.path = 'LearningData/rotation'

        if ver == 1:
            self.path = 'LearningData/rotation'
        elif ver == 2:
            self.path = 'LearningData/speed'
        else:
            self.path = 'LearningData/vertical'

        #Current file directory
        self.my_directory = os.path.join(os.getcwd(), self.path)
        print(self.my_directory)

        # Creating a new folder from new data collection sesion
        while os.path.exists(os.path.join(self.my_directory,f'IMG{str(self.folder_counter)}')):
            self.folder_counter += 1
        # Variable wich new folder directory   
        self.new_folder_path = self.my_directory +"/IMG"+str(self.folder_counter)
        os.makedirs(self.new_folder_path)

    def save_IMG(self,rotation,speed,vertical):
        now = datetime.now()
        timestamp = str(datetime.timestamp(now)).replace('.','')
        #Data simplification for speed
        if speed > 0.1 and speed < 0.7:
            speed = 0.2
        elif speed > 0.7:
            speed = 0.6
        else:
            speed = 0
        

        #Data simplifications for the turn
        if rotation > 0:
            if rotation > 0.5:
                rotation = 0.6
            else:
                rotation = 0.4
        elif rotation == 0:
            rotation == 0
        else:
            if rotation < -0.5:
                rotation = -0.6
            else:
                rotation = -0.4
        #Data simplifications for vertical movement
        if vertical > 0:
            vertical = 1
        elif vertical == 0:
            vertical = 0
        else:
            vertical = -1

        self.rotation_angle_list.append(rotation)
        self.speed_list.append(speed)
        self.v_list.append(vertical)

        file_name = os.path.join(self.new_folder_path,f'IMG_{timestamp}.jpg')
        Camera.capture_file(file_name)
        self.img_list.append(file_name)

    # Creating a log to a photo file
    def create_log_file(self):
        if self.version == 1:
            raw_data = {'Image': self.img_list,
                    'value': self.rotation_angle_list}
        elif self.version == 2:
            raw_data = {'Image': self.img_list,
                    'value': self.speed_list}
        else:
            raw_data = {'Image': self.img_list,
                    'value': self.v_list}
        new_log = pd.DataFrame(raw_data)
        new_log.to_csv(os.path.join(self.my_directory,f'log_{str(self.folder_counter)}.csv'),index=False,header=False)
        print("New log was created and sawed")
        print("Total number of collected images: ",len(self.img_list))

"""global img_list, s_list
folder_counter = 0
img_list = []
rotation_angle_list = []

#Current file directory
my_directory = os.path.join(os.getcwd(), 'LearningData')
print(my_directory)

# Creating a new folder from new data collection sesion
while os.path.exists(os.path.join(my_directory,f'IMG{str(folder_counter)}')):
    folder_counter += 1
new_folder_path = my_directory +"/IMG"+str(folder_counter)
os.makedirs(new_folder_path)


# Function called to collect data
def data_collector(record = 0):
    while True:
        r_val = Controler.rotation
        #print(r_val)
        if record == 0:
            print("Rocording started......")
            record += 1
            time.sleep(300)
        if record == 1:
            img = Camera.capture_file()
            save_IMG(img,r_val)
            time.sleep(300)
        elif record == 2:
            create_log_file()

# Sawing image to folder
def save_IMG(img,rotation):
    global img_list, s_list
    now = datetime.now()
    timestamp = str(datetime.timestamp(now)).raplace('.','')
    file_name = os.path.join(new_folder_path,f'IMG_{timestamp}.jpg')
    cv2.imwrite(file_name, img)
    img_list.append(file_name)
    rotation_angle_list.append(rotation) 

# Creating a log to a photo file
def create_log_file():
    global img_list, rotation_angle_list
    raw_data = {'Image': img_list,
               'rotation': rotation_angle_list}
    new_log = pd.DataFrame(raw_data)
    new_log.to_csv(os.path.join(my_directory,f'log_{str(folder_counter)}.csv'),index=False,header=False)
    print("New log was created and sawed")
    print("Total number of collected images: ",len(img_list))"""


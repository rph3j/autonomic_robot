import cv2
import Camera
import numpy as np
import HatControl as HT
from tensorflow.keras.models import load_model 
from keras.losses import MeanSquaredError
from time import sleep
jeepMotor = HT.HatControler()

sensitivity = 1
speedPer = 0.2
ifAuto = False


model_v1 = load_model('/home/rph3j/Magisterka/Learning/model_rotation_v1.h5', custom_objects ={ "mse" : MeanSquaredError() })
s_model_v1 = load_model('/home/rph3j/Magisterka/Learning/model_speed_v1.h5', custom_objects ={ "mse" : MeanSquaredError() })
a_model = load_model('/home/rph3j/Magisterka/Learning/model_rotation.h5', custom_objects ={ "mse" : MeanSquaredError() })
s_model = load_model('/home/rph3j/Magisterka/Learning/model_speed.h5', custom_objects ={ "mse" : MeanSquaredError() })
v_model = load_model('/home/rph3j/Magisterka/Learning/model_vertical.h5', custom_objects ={ "mse" : MeanSquaredError() })


def preProcess(img):
    img = img[54:120,:,:]
    img = cv2.cvtColor(img,cv2.COLOR_RGB2YUV) #proces show by Nvidia
    img = cv2.GaussianBlur(img,(3,3),0)
    img = cv2.resize(img,(200,66))
    img = img/255
    return img

def stertAuto():
    global ifAuto
    while ifAuto:
        img = Camera.getIMG()
        img = np.asarray(img)
        img = preProcess(img)
        img = np.array([img])
        angle = round(float(model_v1.predict(img)),2)
        print(angle*sensitivity)
        jeepMotor.run(speedPer,-angle)
        cv2.waitKey(1)
    if not ifAuto:
        jeepMotor.stop()

def stertAuto_v2():
    global ifAuto
    while ifAuto:
        img = Camera.getIMG()
        img = np.asarray(img)
        img = preProcess(img)
        img = np.array([img])

        angle = round(float(model_v1.predict(img)),2)
        speed = float(s_model_v1.predict(img))
        #vertical = v_model.predict(img)
        print("Prędkość",speed)
        print("Skęt",angle)
        if round(angle,1) > 0 and round(speed,2) < 0.1:
            speed = -0.2
        if round(speed,3) < 0.01:
            autoChange(False)
        else:
            jeepMotor.run(-speed,-angle)
        #i = np.argmax(vertical[0])
       # d = [-1,0,1][i]
       # print(vertical)
        #print("Weertykalnie",d)
        """if round(vertical) != 0:
            sleep(1)
            autoChange(False)"""
        sleep(0.0001)
    if not ifAuto:
        jeepMotor.stop()

def autoChange(v):
    global ifAuto
    ifAuto = v
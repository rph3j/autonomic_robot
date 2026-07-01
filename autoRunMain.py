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
a_model = load_model('/home/rph3j/Magisterka/Learning/model_rotation.h5', custom_objects ={ "mse" : MeanSquaredError() })
s_model = load_model('/home/rph3j/Magisterka/Learning/model_speed.h5', custom_objects ={ "mse" : MeanSquaredError() })
v_model = load_model('/home/rph3j/Magisterka/Learning/model_vertical.h5')


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
    v_count = 0
    s_count = 0
    while ifAuto:
        img = Camera.getIMG()
        img = np.asarray(img)
        img = preProcess(img)
        img = np.array([img])

        angle = round(float(a_model.predict(img)),2)
        speed = round(float(s_model.predict(img)),2)
        vertical = v_model.predict(img)
        if speed > 0:
            jeepMotor.run(speedPer,-angle)
        else:
            if s_count < 3:
                s_count += 1
            else:
                autoChange(False)
                s_count = 0
        v_i = np.argmax(vertical[0])
        v_d = [-1,0,1][v_i]
        print(vertical)
        print("Weertykalnie",v_d)
        if round(v_d) != 0:
            if v_count < 3:
                v_count += 1
            else:
                jeepMotor.run(speedPer,0,v_d)
                sleep(1)
                autoChange(False)
                v_count = 0
        sleep(0.001)
    if not ifAuto:
        jeepMotor.stop()

def autoChange(v):
    global ifAuto
    ifAuto = v
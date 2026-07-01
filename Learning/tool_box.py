import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.utils import shuffle
import cv2
from datetime import datetime


from tensorflow.keras.optimizers import Adam
from tensorflow.keras.models import Sequential 
from tensorflow.keras.layers import Convolution2D, Flatten, Dense
from tensorflow.keras.losses import Huber

import matplotlib.image as mpIMG
from imgaug import augmenters as iaa

import random
plots_path = "/home/rph3j/Magisterka/Learning/plots"
#Importing the data
def getName(path):
    pathL = path.split('/')[-2:]
    returnPath = os.path.join(pathL[0],pathL[1])
    return returnPath

def importDataInfo(path):
    columns = ['Center','Value']
    rangeOfData = len(os.listdir(path))//2
    data = pd.DataFrame()
    for x in range(0,rangeOfData):
        newData = pd.read_csv(os.path.join(path,f'log_{x}.csv'), names = columns)
        print(f'{x}:{newData.shape[0]}', end='')
        #Only IMG name!!!
        newData['Center'] = newData['Center'].apply(getName)
        #data = data.append(newData,True)
        data = pd.concat([data, newData],ignore_index=True)
        #data.loc[len(data)] = newData
    print(" ")
    print('Total Images Imported', data.shape[0])
    return data

#Data regulation
def dataRegulation(data,t,samples = 200, dispaly =True):
    global plots_path
    nBin = 31
    hist, bins = np.histogram(data['Value'], nBin)
    if dispaly:
        center = (bins[:-1] + bins[1:]) * 0.5
        plt.bar(center, hist, width=0.03)
        plt.plot((np.min(data['Value']),np.max(data['Value'])),(samples,samples))
        plt.title("Raw" + t)
        plt.xlabel("Value")
        plt.ylabel("Number of samples")
        p_new = os.path.join(plots_path,"Raw_"+t+".png")
        plt.savefig(p_new)
        plt.close()


    remIndex = []
    for j in range(nBin):
        binDataList = []
        for i in range(len(data['Value'])):
            if data['Value'][i] >= bins[j] and data['Value'][i] <= bins[j + 1]:
                binDataList.append(i)
        binDataList = shuffle(binDataList)
        binDataList = binDataList[samples:]
        remIndex.extend(binDataList)

    print("IMG removed from learning list: ", len(remIndex))
    data.drop(data.index[remIndex],inplace=True)
    print('IMG in revised list', len(data))

    if dispaly:
        hist, _ = np.histogram(data['Value'], (nBin))
        plt.bar(center,hist,width=0.03)
        plt.plot((np.min(data['Value']),np.max(data['Value'])),(samples,samples))
        plt.title("Revised " +t)
        plt.xlabel("Value")
        plt.ylabel("Number of samples")
        p_new = os.path.join(plots_path,"Revised_"+t+".png")
        plt.savefig(p_new)
        plt.close()
    return data

# Data preparation
def loadData(path,data):
    pathIMG = []
    angle = []
    for i in range(len(data)):
        i_data = data.iloc[i]
        pathIMG.append(os.path.join(path,i_data['Center']))
        angle.append(float(i_data['Value']))
    pathIMG = np.asarray(pathIMG)
    angle = np.asarray(angle)
    return pathIMG, angle

#Augment (randomly added zoom, translation, flip, brightnes)

def a_IMG(imgPath,value,ver):
    img = mpIMG.imread(imgPath)
    if np.random.rand() < 0.5:
        pan = iaa.Affine(translate_percent={"x":(-0.1,0.1),"y":(-0.1,0.1)})
        img = pan.augment_image(img)
    if np.random.rand() < 0.5:
        zoom = iaa.Affine(scale=(1,1.2))
        img - zoom.augment_image(img)
    if np.random.rand() < 0.5:
        brightnes = iaa.Multiply((0.5,1.2))
        img =  brightnes.augment_image(img)
    if np.random.rand() < 0.5:
        img = cv2.flip(img,1)
        if ver == 1:
            value = -value
        elif ver == 3:
            if value == 0: value = 2
            elif value == 2: value = 0
    return img, value

#Procesing
def preProcess(img):
    img = img[54:120,:,:]
    img = cv2.cvtColor(img,cv2.COLOR_RGB2YUV) #proces show by Nvidia
    img = cv2.GaussianBlur(img,(3,3),0)
    img = cv2.resize(img,(200,66))
    img = img/255
    return img


#create model for training
def createModel(ver, lr = 0.0001):
    model = Sequential()
    model.add(Convolution2D(24, (5,5),(2,2), input_shape=(66,200,3),activation='elu'))
    model.add(Convolution2D(36,(5,5),(2,2),activation='elu'))
    model.add(Convolution2D(48,(5,5),(2,2),activation='elu'))
    model.add(Convolution2D(64,(3,3),activation='elu'))
    model.add(Convolution2D(64,(3,3),activation='elu'))

    model.add(Flatten())
    model.add(Dense(100, activation='elu'))
    model.add(Dense(50, activation='elu'))
    model.add(Dense(10, activation='elu'))
    if ver == 3:
        model.add(Dense(3,activation='softmax'))
        model.compile(optimizer=Adam(learning_rate=lr),loss='sparse_categorical_crossentropy',metrics=['accuracy'])
    else:
        model.add(Dense(1))
        model.compile(optimizer=Adam(learning_rate=lr),loss='mse')
    return model
#Random selection from training data pool
def d_gen(imgPath,angles,bathSize,flag,ver=1):
    while True:
        imgBath = []
        angelsBath = []

        for i in range(bathSize):
            ix = random.randint(0,len(imgPath)-1)
            if flag:
                img, angle = a_IMG(imgPath[ix],angles[ix],ver)
            else:
                img = mpIMG.imread(imgPath[ix])
                angle = angles[ix]
            img = preProcess(img)
            imgBath.append(img)
            angelsBath.append(angle)
            #print(angelsBath)
        yield (np.asarray(imgBath),np.asarray(angelsBath))
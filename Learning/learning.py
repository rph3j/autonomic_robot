print('start learning .....')
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] ='3'
from sklearn.model_selection import train_test_split
from tool_box import *

status = 0
progres = 0

def learn(ver=1,lr=0.0001,epoch=10,samples = 200):
    global status
    global progres
    global plots_path 
    if ver == 1:
        name = 'rotation'
    elif ver == 2:
        name = 'speed'
    else:
        name = 'vertical'
    # 1 - colecting the Data from LearningData folder
    status = "Zaczytywanie danych"
    progres = 10
    path = '/home/rph3j/Magisterka/LearningData/' + name
    data = importDataInfo(path)
    print(data.head())

    # 2 - Data revision
    status = "Sprawdzanie danych"
    progres = 20
    data = dataRegulation(data,name+"_data",samples)
    print(data.head())

    # 3 - Data preparation
    status = "Przygotowanie danych"
    progres = 30
    p_img, values = loadData(path,data)

    #4 - preapre date for training
    status = "Przygotowanie podziału treningowego"
    progres = 40
    xTrain, xVal, yTrain, yVal = train_test_split(p_img,values, test_size=0.2,random_state=10)
    print("Totla training: ", len(xTrain))
    print("Total validiation: ",len(xVal))
    print(yTrain)
    # vertical movement mapping
    if ver == 3:
        mapping = {-1: 0, 0: 1, 1: 2}
        yTrain = [mapping[y] for y in yTrain]
        yVal = [mapping[y] for y in yVal]
        #print( yTrain )
        #print(yVal)

    #5 -Creating model
    status = "Tworzenie modelu"
    progres = 50
    model = createModel(ver,lr)

    #6 - main learning
    status = "Uczenie"
    progres = 60
    m_h =  model.fit(d_gen(xTrain,yTrain,100,1,ver),
                steps_per_epoch=100,
                epochs=epoch,
                validation_data = d_gen(xVal,yVal,50,0,ver),
                validation_steps=50)

    #7 - saving the model
    status = "Zapisywanie modelu"
    progres = 90
    model.save('model_'+name+'.h5')
    print('Model Saved')

    #8 - generating learning plot
    status = "Przygotowanie wykresu błędu"
    progres = 95
    plt.plot(m_h.history['loss'])
    plt.plot(m_h.history['val_loss'])
    plt.legend(['Training','Validation'])
    plt.title('Loss_'+name)
    plt.xlabel('Epoch')
    p_new = os.path.join(plots_path,"Learning_Plot_"+name+".png")
    plt.savefig(p_new)
    plt.close()

    status = "Koniec"
    progres = 100

if __name__ == '__main__':
    #learn(2,1e-4,10,500) # zmieniona koncepcja
    learn(3,1e-4,20,400)
    #learn(1,1e-4,30,450)
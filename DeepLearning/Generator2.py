import numpy as np

import os

import sys
import glob

import random
import cv2
from PIL import Image

#import keras.backend as K
from keras import models
from keras import callbacks
import incept
import resnet50
from keras.models import load_model

from keras import callbacks
from keras.preprocessing import image

train_path = 'C:\\Users\\Bilgehan\\Documents\\three_class_ny2\\train\\Hard_Left'
valid_path = 'C:\\Users\\Bilgehan\\Documents\\three_class_ny2\\val\\Hard_Right'
test_path = 'C:\\Users\\Bilgehan\\Documents\\three_class_ny2\\test\\Hard_Right'


def train(train_path, valid_path, test_path, preprocess=1, batch_size=32, epochs=5, verbose=1, img_size=-1,
          checkpoint=None,
          all_train_test=1, get_model=None):
    test_images = []

    test_labels = []

    path4 = []
    model = None
    path3 = []
    path6 = []
    y_labels = []
    val_labels =[]

    valid_imagess = []


    if all_train_test == 0 or all_train_test==1:
        for name in glob.glob1(train_path, '*jpg'): #Training get data
            path2 = os.path.join(train_path, name)
            path3.append(path2)

            steering = name[:-4]

            steering = steering.replace(',', '.')

            steering = steering.split('_')
            steering = float(steering[4])

            y_labels.append(steering)

        for name_y in glob.glob1(valid_path, '*jpg'):  # Validation get data
            path5 = os.path.join(valid_path, name_y)
            path6.append(path5)

            steering_val = name_y[:-4]
            steering_val = steering_val.replace(',', '.')

            steering_val = steering_val.split('_')

            steering_val = float(steering_val[4])

            val_labels.append(steering_val)
    if all_train_test == 0 or all_train_test==2:
        for i in glob.glob1(test_path, '*jpg'):  # Test get data
            path_test = os.path.join(test_path, i)
            path4.append(path_test)

            steering = i[:-4]
            steering = steering.replace(',', '.')

            steering = steering.split('_')
            steering = float(steering[4])
            test_labels.append(steering)

    '''
    def shuffle_images(path3, y_labels):
        shuffle = list(zip(path3, y_labels))
        random.shuffle(shuffle)
        path3, y_labels = zip(*shuffle)
    
        trainx = path3[:int(len(path3) * 0.8)]
        trainy = y_labels[:int(len(y_labels) * 0.8)]
    
        valx = path3[-int(len(path3) * 0.2):]
        valy = y_labels[-int(len(y_labels) * 0.2):]
        return trainx, trainy, valx, valy
    '''


    for y in path6:  # Validation preprocess
        valid_images = cv2.imread(y)
        if img_size != -1:
            valid_images = cv2.resize(valid_images, img_size)
            print("CORRECT")
        valid_images = cv2.cvtColor(valid_images, cv2.COLOR_BGR2RGB)
        if preprocess == 1:
            valid_images = valid_images.astype('float') / 255.0
        elif preprocess == 0:
            valid_images = valid_images.astype('float') / 127.5 - 1
        valid_images = np.array(valid_images)
        # valid_images = np.expand_dims(valid_images, axis=0)
        valid_imagess.append(valid_images)

    valid_imagess = np.array(valid_imagess)


    for tt in path4:
        test_image = cv2.imread(tt)
        if img_size != -1:
            test_image = cv2.resize(test_image, img_size)
        test_image = cv2.cvtColor(test_image, cv2.COLOR_BGR2RGB)
        if preprocess == 1:
            test_image = test_image.astype('float') / 255.0
        elif preprocess == 0:
            test_image = test_image.astype('float') / 127.5 - 1
        test_image = np.array(test_image)
        test_images.append(test_image)

    test_images = np.array(test_images)




    def generate_batch(): # Training preprocess


        gen_state = 0

        while True:
            XX = []
            if len(path3) < gen_state+batch_size:
                gen_state = 0

            paths = path3[gen_state: gen_state + batch_size]
            y = y_labels[gen_state: gen_state + batch_size]

            for x in paths:
                X = cv2.imread(x)
                if img_size != -1:
                    X = cv2.resize(X, img_size)
                X = cv2.cvtColor(X, cv2.COLOR_BGR2RGB)
                if preprocess == 1:
                    X = X.astype('float') / 255.0
                elif preprocess == 0:
                    X = X.astype('float') / 127.5 - 1
                X = np.array(X)
                #X = np.expand_dims(X, axis=0)
                XX.append(X)

            gen_state += batch_size
            yield np.array(XX), np.array(y)




    #model = resnet50.get_model()
    X, y = valid_imagess, val_labels

    if all_train_test==2:
        model = load_model("weights.01-33.97.hdf5")
    if all_train_test==0 or all_train_test==1:
        model = get_model
        if checkpoint is None:
            model.fit_generator(generate_batch(),
                                validation_data=(X, y), steps_per_epoch=len(path3)//batch_size, epochs=epochs, verbose=verbose)
        else:
            model.fit_generator(generate_batch(),
                                validation_data=(X, y), steps_per_epoch=len(path3) // batch_size, epochs=epochs,
                                verbose=verbose, callbacks=[checkpoint])

    if all_train_test==0 or all_train_test==2:
        predicted = model.predict(test_images)

        for ix in range(len(test_labels)):
            print("X=%s, Predicted=%s" % (test_labels[ix], predicted[ix]))


if __name__ == '__main__':

    checkpoint_path = "weights.{epoch:02d}-{val_loss:.2f}.hdf5"
    check = callbacks.ModelCheckpoint(checkpoint_path, verbose=1,
                                           save_best_only=True,
                                           save_weights_only=False,
                                           mode='auto')

    train(train_path=train_path, valid_path=valid_path, test_path=test_path, preprocess=1, batch_size=64, epochs=5, verbose = 1, img_size=-1, checkpoint=check,
            all_train_test=2, get_model=resnet50.get_model())

import time
import keras
start_time = time.time()
from keras.models import Sequential
from keras.layers import Dense, Dropout, Flatten, Activation
from keras.layers import Conv2D, MaxPooling2D
from keras.preprocessing.image import ImageDataGenerator
from keras import backend as K
from keras import applications
from keras.models import Model

# Only Hard_Left, Hard_Right and Straight
train_data_dir = 'D:\\Datasets\\arti_sim\\three_class\\train'
validation_data_dir = 'D:\\Datasets\\arti_sim\\three_class\\val'

# Dimension of the images
img_width, img_height = 250, 90

# input_shape = (90, 250, 3)

# Config
epoch = 5
batch_size = 24
num_classes = 3

# Dataset
nb_train_samples = 3329
nb_validation_samples = 1664

# Saving model
save_model = False

# Channel input
if K.image_data_format() == 'channels_first':
    input_shape = (3, img_width, img_height)
else:
    input_shape = (img_width, img_height, 3)

print('Input shape = ', input_shape)

# Creating a small convolutional neural network (NVIDIA architecture)
# model = Sequential()
# model.add(Conv2D(24, (5, 5), strides=(2, 2),  input_shape=input_shape, data_format='channels_last'))
# model.add(Activation('relu'))
#
# # First block
# model.add(Conv2D(32, (5, 5), strides=(2, 2)))
# model.add(Activation('relu'))
#
# # Second block
# model.add(Conv2D(64, (5, 5), strides=(2, 2)))
# model.add(Activation('relu'))
#
# #Third block
# model.add(Conv2D(64, (3, 3), strides=(1, 1)))
# model.add(Activation('relu'))
#
# #Forth block
# model.add(Conv2D(64, (3, 3), strides=(1, 1)))
# model.add(Activation('relu'))

# build the VGG16 network
base_model = applications.VGG16(weights='imagenet', include_top=False, input_shape=input_shape)

# Fully connected layers / Classifier
top_model = Sequential()
top_model.add(Flatten(input_shape=base_model.output_shape[1:]))
top_model.add(Dense(100, activation='relu'))
top_model.add(Dropout(0.40))
top_model.add(Dense(50, activation='relu'))
top_model.add(Dropout(0.20))
top_model.add(Dense(num_classes, activation='softmax'))

model = Model(inputs=base_model.input, outputs=top_model(base_model.output))
# Compiles the model with loss and optimization function
model.compile(loss=keras.losses.categorical_crossentropy,
              optimizer=keras.optimizers.Adadelta(),
              metrics=['accuracy'])

# This is the augmentation configuration we will use for training
train_datagen = ImageDataGenerator(
    rescale=1. / 255,
    shear_range=0.2,
    zoom_range=0.2,
    horizontal_flip=True)

# We use no augmentation configuration for validation:
# only rescaling the RGB to float between 0 and 1.
validation_datagen = ImageDataGenerator(rescale=1. / 255)

# Reading the training images from the given path
train_generator = train_datagen.flow_from_directory(
    train_data_dir,
    target_size=(img_width, img_height),
    batch_size=batch_size,
    class_mode='categorical')

# Reading the validation images from the given path
validation_generator = validation_datagen.flow_from_directory(
    validation_data_dir,
    target_size=(img_width, img_height),
    batch_size=batch_size,
    class_mode='categorical')


model.summary()

# Training the model
model.fit_generator(
    train_generator,
    steps_per_epoch=nb_train_samples // batch_size,
    epochs=epoch,
    verbose=1,
    validation_data=validation_generator,
    validation_steps=nb_validation_samples // batch_size)

# Saving the model/weights
if save_model:
    model.save('Artibot.model')
    model.save('Artibot_weights.h5')
    print('Model saved')
else:
    print('Model not saved')


del model
K.clear_session()

timer = time.time()
print("Minutes used to run script: ")
print((timer - start_time)/60)

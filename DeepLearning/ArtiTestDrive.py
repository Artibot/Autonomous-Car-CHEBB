# Libraries
import time
import keras
start_time = time.time()
from keras.models import Sequential
from keras.layers import Dense, Dropout, Flatten, Activation
from keras.layers import Conv2D, MaxPooling2D
from keras.preprocessing.image import ImageDataGenerator
from keras import backend as K
from keras.callbacks import ModelCheckpoint


# Destination to save model
# model_path = "C:\\Users\\Chrisander\\Desktop\\untitled\\VGG16_models\\"
model_path = "C:\\Users\\Chrisander\\Desktop\\untitled\\2828_models\\"
# Dimension of the images
img_width, img_height = 28, 28

# Dataset path
train_data_dir = 'D:\\Datasets\\arti_sim\\three_class_ny2\\train'
validation_data_dir = 'D:\\Datasets\\arti_sim\\three_class_ny2\\val'

# Dataset
nb_train_samples = 7975
nb_validation_samples = 3913

# Config
epoch = 40
batch_size = 24
num_classes = 3

# Saving model
save_model = False

# Channel input
if K.image_data_format() == 'channels_first':
    input_shape = (3, img_width, img_height)
else:
    input_shape = (img_width, img_height, 3)

print('Input shape = ', input_shape)

# Creating a small convolutional neural network (VGG architecture)
model = Sequential(name="baseTest")
model.add(Conv2D(32, (3, 3), input_shape=input_shape, data_format='channels_last', name="inputTest"))
model.add(Activation('relu'))
model.add(MaxPooling2D(pool_size=(2, 2)))

# First block
model.add(Conv2D(64, (3, 3)))
model.add(Activation('relu'))
model.add(MaxPooling2D(pool_size=(2, 2)))

# Second block
model.add(Conv2D(128, (3, 3)))
model.add(Activation('relu'))
model.add(MaxPooling2D(pool_size=(2, 2)))
model.add(Dropout(0.05))

# Fully connected layers / Classifier
model.add(Flatten())
model.add(Dense(100, activation='relu'))
model.add(Dropout(0.40))
model.add(Dense(num_classes, activation='softmax', name="outputTest"))

# Compiles the model with loss and optimization function
model.compile(loss=keras.losses.categorical_crossentropy,
              optimizer=keras.optimizers.Adadelta(),
              metrics=['accuracy'])

model.summary()
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

# Path + name of the model we're saving
# filepath = model_path + "ArtiTest_3Class_EP{epoch:02d}-{val_loss:.2f}-{val_acc:.2f}.h5"
filepath = model_path + "Arti2828_2nd-VL_{val_loss:.2f}-VA_{val_acc:.2f}.h5"
# minimum change in the monitored quantity to qualify as an improvement,
# i.e. an absolute change of less than min_delta, will count as no improvement.
min_delta = 0.0005  #

# Save best model in form of validation loss
checkpoint = ModelCheckpoint(filepath, monitor='val_loss', verbose=1, save_best_only=True, mode='min')

# Stops the training of the model if the validation loss is not improving.
early_stop = keras.callbacks.EarlyStopping(monitor='val_loss',
                                           min_delta=min_delta,
                                           patience=5,
                                           verbose=1,
                                           mode='auto')

callbacks_list = [checkpoint, early_stop]

# Training the model
model.fit_generator(
    train_generator,
    steps_per_epoch=nb_train_samples // batch_size,
    epochs=epoch,
    verbose=1,
    validation_data=validation_generator,
    validation_steps=nb_validation_samples // batch_size,
    callbacks=callbacks_list)

# Saving the model/weights
if save_model:
    model.save('ArtiTest.model')
    model.save('ArtiTest.h5')
    print('Model saved')
else:
    print('Model not saved')


del model
K.clear_session()

timer = time.time()
print("Minutes used to run script: ")
print((timer - start_time)/60)


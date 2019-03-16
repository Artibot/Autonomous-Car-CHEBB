# Libraries
import keras
from keras.models import Sequential
from keras.layers import Dense, Dropout, Flatten, Activation
from keras.layers import Conv2D, MaxPooling2D
from keras.preprocessing.image import ImageDataGenerator
from keras import backend as K
import Generator2


# Dimension of the images
img_width, img_height = 48, 48

# Dataset path
train_data_dir = "D:\\Datasets\\Regression_Artibot\\train"
validation_data_dir = "D:\\Datasets\\Regression_Artibot\\val"
test_data_dir = ""

# Config
epoch = 20
batch_size = 24
num_classes = 2
width, height = 48, 48
# Saving model
save_model = False

# Channel input
input_shape = (width, height, 3)

# if K.image_data_format() == 'channels_first':
#     input_shape = (3, img_width, img_height)
# else:
#     input_shape = (img_width, img_height, 3)

# input_shape = (1, 28, 28)
print('Input shape = ', input_shape)
model = Sequential()
model.add(Conv2D(32, (3, 3), input_shape=input_shape, data_format='channels_last'))
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

# Third block
model.add(Conv2D(256, (3, 3)))
model.add(Activation('relu'))
model.add(MaxPooling2D(pool_size=(2, 2)))
model.add(Dropout(0.20))

# Classifier
model.add(Flatten())
model.add(Dense(256, activation='relu'))
model.add(Dropout(0.40))
# model.add(Dense(num_classes, activation='linear'))
model.add(Dense(num_classes))

# Compile
model.compile(loss=keras.losses.MSE,
              optimizer=keras.optimizers.Adagrad(),
              metrics=['accuracy'])


Generator2.train(train_path=train_data_dir, valid_path=validation_data_dir, test_path=test_data_dir,
                 preprocess=1, batch_size=batch_size, epochs=epoch, verbose=1, img_size=(width, height),
                 all_train_test=1, checkpoint=None, get_model=model)
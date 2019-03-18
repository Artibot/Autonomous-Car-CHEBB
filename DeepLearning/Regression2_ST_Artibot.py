from keras.models import Sequential
from keras.layers import Dense, Dropout, Flatten, Activation
from keras.layers import Conv2D, MaxPooling2D
from keras.preprocessing.image import ImageDataGenerator
import Generator3
from keras import applications
from keras.models import Model
from keras.callbacks import ModelCheckpoint
import keras


# --------- OLD DATA SET (3 CLASS CLASSIFICATION) ------------
# train_dirr = "D:\\Datasets\\arti_sim\\Regression\\train"
# val_dirr = "D:\\Datasets\\arti_sim\\Regression\\val"


# ------------------ FIRST REGRESSION DATA SET -------------------
# train_dirr = "D:\\Datasets\\arti_sim\\Regression\\steering\\train"
# val_dirr = "D:\\Datasets\\arti_sim\\Regression\\steering\\val"


# ------------------ SECOND REGRESSION DATA SET -------------------
train_dirr = "D:\\Datasets\\arti_sim\\Regression\\steering_throttle\\train"
val_dirr = "D:\\Datasets\\arti_sim\\Regression\\steering_throttle\\val"
test_dirr = "hei3"


model_path = "C:\\Users\\Chrisander\\Desktop\\untitled\\Regression_models\\"
model_name = "VGG16_Regression_ST_4th.EP{epoch:02d}-{val_loss:.2f}-{val_acc:.2f}.h5"


width, height = 48, 48
batch_size = 24
epochs = 300
num_classes = 2



input_shape = (width, height, 3)

# VGG16
base_model = applications.VGG16(weights='imagenet', include_top=False, input_shape=input_shape)

# Fully connected layers / Classifier
top_model = Sequential()
top_model.add(Flatten(input_shape=base_model.output_shape[1:], name="InputVGG"))
top_model.add(Dense(100, activation='relu'))
top_model.add(Dropout(0.40))
top_model.add(Dense(50, activation='relu'))
top_model.add(Dropout(0.20))
top_model.add(Dense(num_classes, activation='linear', name="OutputVGG"))

model = Model(inputs=base_model.input, outputs=top_model(base_model.output))


for layer in model.layers[:-3]:
    layer.trainable = False


model.compile(loss=keras.losses.MSE,
              optimizer=keras.optimizers.Adagrad(),
              metrics=['accuracy'])

model.summary()

# Path + name of the model we're saving
filepath = model_path + model_name

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

#callback_list = [checkpoint, early_stop]

callback_list = checkpoint

Generator3.train(train_path=train_dirr, valid_path=val_dirr, test_path=test_dirr, preprocess=1,
                 batch_size=batch_size, epochs=epochs, verbose=1, img_size=(width, height), checkpoint=callback_list,
                all_train_test=1, get_model=model)


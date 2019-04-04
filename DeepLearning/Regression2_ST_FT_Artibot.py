import Generator3
from keras.models import load_model
from keras.callbacks import ModelCheckpoint
import keras
import os


# train_dirr = "D:\\Datasets\\arti_sim\\Regression\\train"
# val_dirr = "D:\\Datasets\\arti_sim\\Regression\\val"
test_dirr = "hei3"


train_dirr = "D:\\Datasets\\arti_sim\\Regression\\steering_throttle\\train"
val_dirr = "D:\\Datasets\\arti_sim\\Regression\\steering_throttle\\val"

model_transfer = "VGG16_Regression_ST_4th.EP284-0.70-0.92.h5"

model_path = "C:\\Users\\Chrisander\\Desktop\\untitled\\Regression_models\\"
model_save_name = "VGG16_Regression_ST_FT_1st.EP{epoch:02d}-{val_loss:.2f}-{val_acc:.2f}.h5"

filepath_model = os.path.join(model_path, model_transfer)

width, height = 48, 48
batch_size = 24
epochs = 300

input_shape = (width, height, 3)

model = load_model(filepath_model)

for layer in model.layers[:-1]:
    layer.trainable = False


model.summary()

# Path + name of the model we're saving
filepath = model_path + model_save_name

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


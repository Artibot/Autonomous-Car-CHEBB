from keras.preprocessing.image import ImageDataGenerator
from tensorflow import keras
from keras.models import load_model
import numpy as np
import os
k = keras.backend

# Path to desired model
file_path = "C:\\Users\\Chrisander\\Desktop\\untitled\\VGG16_models"
model_name = "FT_VGG16_3Class.EP19-Train0.88-Val_Loss0.23-Val_Acc0.92.h5"
model_path = os.path.join(file_path, model_name)

# Path to Data-set
test_data_dir = 'D:\\Datasets\\arti_sim\\three_class_ny2\\test'

# Batch size
batch_size_test = 32

# Dimension of images / Input shape
img_width, img_height = 90, 250

# RGB channel converted to float between 0 and 1
test_gen = ImageDataGenerator(rescale=1. / 255)

test_generator = test_gen.flow_from_directory(
    test_data_dir,
    target_size=(img_height, img_width),
    batch_size=batch_size_test,
    shuffle=False,
    class_mode='categorical')

num_test_batches = np.ceil(test_generator.samples // batch_size_test)

model = load_model(model_path)
model_score = model.evaluate_generator(test_generator, steps=num_test_batches)
print('Evaluating model')
print(model.metrics_names)
print(model_score)
print('Model scored ' + str(model_score[1]*100) + '% accuracy')
del model
k.clear_session()
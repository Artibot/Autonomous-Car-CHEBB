from keras import backend as k
from keras.models import load_model
import numpy as np
import cv2
import glob
import os
import time

model_path = 'FT_VGG16_3Class_EP19-Train0,88-Val_Loss0.23-Val_Acc0,92.h5'
test_path = 'D:\\Datasets\\arti_sim\\three_class_ny2\\test\\Straight'
image_path = '/home/chrisander/datasets//MNIST/testing/0/10.png'
nb_images = 182





start_time = time.time()
for name in glob.glob1(test_path, '*.jpg'):
    path = os.path.join(test_path, name)

    image = cv2.imread(path)
    #plot_image = image
    image = cv2.resize(image, (90, 250))
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    image = image.astype('float') / 255.0
    image = np.array(image)
    image = np.expand_dims(image, axis=0)

    model = load_model(model_path)
    model_score = model.predict(image)
    model_score = np.argmax(model_score)
    # print('Prediction: ' + str(model_score) + ', Image: ' + str(path))
    #
    #
    # plot_image = cv2.resize(plot_image, (400, 400))
    # font = cv2.FONT_HERSHEY_SIMPLEX
    # text = 'Prediction: ' + str(model_score)
    # cv2.putText(plot_image, text, (10, 390), font, 1, (0, 0, 255), 2, cv2.LINE_AA)
    # cv2.imshow(text, plot_image)
    # cv2.waitKey(0)
    # # cv2.destroyAllWindows()

end_time = time.time() - start_time
print("FPS: ", nb_images/end_time)
del model
k.clear_session()
import tensorflow as tf
from tensorflow.python.platform import gfile
import cv2
import numpy as np
import keras
from keras.models import load_model

class MyModel:

	model = ""
	img_width = 0
	img_height = 0
	
	def __init__(self, iw, ih, model_name):
		#Initialize model
		self.model = load_model(model_name)
		self.model.summary()
		
		#Set image dimensions
		img_width = iw;
		img_height = ih;	

	def imgToArray(self, im):
		im = cv2.imread("13.png")
		im = cv2.resize(im, (self.img_width, self.img_height))
		im = cv2.cvtColor(im, cv2.COLOR_BGR2RGB)
		im = im.astype('float') / 255.0
		im = np.array(im)
		return np.expand_dims(im, axis=0)
		
	def predictImage(self, image_feed, useArgMax):
		model_score = self.model.predict(self.imgToArray(image_feed))
		if useArgMax:
			model_score = np.argmax(model_score)
		return model_score
	
		

#------------- Create model object ---------------
model1 = MyModel(28, 28, "VGG_MNIST.model")


#------------ Continuous predictions -------------
while(1):
	prediction = model1.predictImage("13.png", True)
	print("Prediction " + str(k) + " is " + str(prediction))


import cv2
import numpy as np
import time
from keras.models import load_model

class MyModel:

	# MyModel(input_layer_width, input_layer_height, model_name)
	def __init__(self, iw, ih, model_name):
		#Initialize model
		self.model = load_model(model_name)
		self.input_layer_width = iw
		self.input_layer_height = ih

	#Predicts target image and returns either a tensor, or an argmax value of the tensor
	def predictImage(self, image_feed, returnTensor=True):
		numpy_image = self.imgToArray(image_feed)
		model_score = self.model.predict(numpy_image)
		if not returnTensor:
			model_score = np.argmax(model_score)
		return model_score

	#Calculates fps with a certain image, returns final FPS
	def calculateFPS(self, im, iters):
		st = time.time()
		for k in range(1, iters+1):
			pred = self.predictImage(im, returnTensor=False)
			if k % 500 == 0:
				print("FPS:", k / (time.time() - st),
					  "          \tIteration:", k,
					  "          \tCurrent prediction:", pred,
					  "          \tReceived image[", cv2.imread(im).shape[1], "x", cv2.imread(im).shape[0], "]")
		return iters / (time.time() - st)

	#Returns normalized np array with RGB from image_feed
	def imgToArray(self, image_feed):
		im = cv2.imread(image_feed)
		if im.shape[0] != 28:
			if im.shape[1] != 28:
				im = cv2.resize(im, (self.input_layer_width, self.input_layer_height))
		im = cv2.cvtColor(im, cv2.COLOR_BGR2RGB)
		im = im.astype('float') / 255.0
		im = np.array(im)
		return np.expand_dims(im, axis=0)
#------------------ END CLASS ---------------------



#Model object
#Loading MyModel object as (layer_input_width, layer_input_height, model_name)
m1 = MyModel(28, 28, "VGG_MNIST.model")


#Calculating FPS with (image_name, iterations)
m1.calculateFPS("13.png", 20000)

#Predicting value with (image_name, returnTensor)
myOutputValue = m1.predictImage("13.png", returnTensor=False)
print(myOutputValue)

#We will use predictImage function and pass image from camera class as argument
#i.e camera.GetImage()
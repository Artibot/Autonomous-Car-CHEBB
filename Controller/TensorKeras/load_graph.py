import cv2
import numpy as np
import time
from keras.models import load_model
import imageCapture as iCap
import sys

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
	def calculateFPS(self, im, iters, frameEval):
		st = time.time()
		abc, vid = cap.read()
		vid = np.array(vid)
		for k in range(1, iters+1):
			if k % frameEval == 0:
				abc, vid = cap.read()
				vid = np.array(vid)
				pred = self.predictImage(vid, returnTensor=False)
			if k % 150 == 0:
				print("FPS:", k / (time.time() - st),
					  "          \tIteration:", k,
					  "          \tCurrent prediction:", pred,
					  "          \tReceived image[", vid.shape[1], "x", vid.shape[0], "]")
		return iters / (time.time() - st)

	#Returns normalized np array with RGB from image_feed
	def imgToArray(self, im):
		#im = cv2.imread(image_feed)
		if im.shape[0] != 28:
			if im.shape[1] != 28:
				im = cv2.resize(im, (self.input_layer_width, self.input_layer_height))
		#im = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
		im = im.astype('float') / 255.0
		im = np.array(im)
		im = np.expand_dims(im, axis=0)
		return im
#------------------ END CLASS ---------------------



#Model object
#Loading MyModel object as (layer_input_width, layer_input_height, model_name)
m1 = MyModel(28, 28, "VGG_MNIST.model")


#Calculating FPS with (image_name, iterations)
#m1.calculateFPS("13.png", 20000)

#Predicting value with (image_name, returnTensor)
#myOutputValue = m1.predictImage("13.png", returnTensor=False)


args = iCap.parse_args()
cap = iCap.open_cam_onboard(args.image_width, args.image_height)
if not cap.isOpened():

	sys.exit('Failed to open camera!')

abc, vid = cap.read()
m1.calculateFPS(np.array(vid), 15000, 8)

#print(cv2.imread("13.png").shape)

#for i in range(1, 50000):	
#	abc, vid = cap.read()
	#print(np.array(vid))
#	val = m1.predictImage(np.array(vid), returnTensor=False)
#	if i % 25 == 0:
#		print("Iteration: ", i, " is ", val)
#	i += 1

cap.release()


#We will use predictImage function and pass image from camera class as argument
#i.e camera.GetImage()

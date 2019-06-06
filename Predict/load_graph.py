import cv2
import numpy as np
import time
from keras.models import load_model
from keras import backend as k
import imageCapture as iCap
import sys
import config


class MyModel:

	# MyModel(input_layer_width, input_layer_height, model_name)
	def __init__(self, iw, ih, model_name):
		#Initialize model
		self.model = load_model(model_name)
		self.input_layer_width = iw
		self.input_layer_height = ih
		print("Model loaded.")
	def delModel(self):
		#k.session_clear()
		del self.model	

	#Predicts target image and returns either a tensor, or an argmax value of the tensor
	def predictImage(self, image_feed, returnTensor=True):
		numpy_image = self.imgToArray(image_feed)
		model_score = self.model.predict(numpy_image)
		if not returnTensor:
			model_score = np.argmax(model_score)
		return model_score[0][0]

	#Calculates fps with a certain image, returns final FPS
	def predictModel(self, im, iters, frameEval):
		st = time.time()
		#abc, vid = cap.read()
		vid = im
		pred = 0
		if iters != 0:
			for k in range(1, iters+1):
				if k % frameEval == 0:
					#abc, vid = cap.read()
					vid = im
					pred = self.predictImage(vid, returnTensor=True)
				if k % 10 == 0:
					print("FPS:", k / (time.time() - st),
						  "          \tIteration:", k,
						  "          \tCurrent prediction:", pred,
						  "          \tReceived image[", vid.shape[1], "x", vid.shape[0], "]")
			return iters / (time.time() - st)
		else:
			k = 0
			while(1):
				if k % frameEval == 0:
					abc, vid = cap.read()
					vid = np.array(vid)
					pred = self.predictImage(vid, returnTensor=config.CONFIG['print_tensor'])
				if k % 10 == 0:
					print("FPS:", k / (time.time() - st),
						  "          \tIteration:", k,
						  "          \tCurrent prediction:", pred,
						  "          \tReceived image[", vid.shape[1], "x", vid.shape[0], "]")
				k += 1			

	#Returns normalized np array with RGB from image_feed
	def imgToArray(self, im):
		#im = cv2.imread(image_feed)
		if im.shape[0] != self.input_layer_width:
			if im.shape[1] != self.input_layer_height:
				im = cv2.resize(im, (self.input_layer_width, self.input_layer_height))
		im = cv2.cvtColor(im, cv2.COLOR_BGR2RGB)
		im = (im.astype('float') / 255)
		im = np.array(im)
		im = np.expand_dims(im, axis=0)
		return im
#------------------ END CLASS ---------------------



#Model object
#Loading MyModel object as (layer_input_width, layer_input_height, model_name)

print("Loading model...\n")
#m1 = MyModel(config.CONFIG['model_width'], config.CONFIG['model_height'], config.CONFIG['model_name'])

#m1 = MyModel(128, 128, "ResNet_steering_FT_150x2.EP11-0.10-0.13.h5")

#Calculating FPS with (image_name, iterations)

#Predicting value with (image_name, returnTensor)
#myOutputValue = m1.predictImage("13.png", returnTensor=False)

#args = iCap.parse_args()
#cap = iCap.open_cam_onboard(args.image_width, args.image_height)
#if not cap.isOpened():

#	sys.exit('Failed to open camera!')

#abc, vid = cap.read()

#if config.CONFIG['Show_Cam']:
#    iCap.open_window(args.image_width, args.image_height)
#    iCap.read_cam(cap)

#m1.predictModel(np.array(vid), config.CONFIG['iterations'], config.CONFIG['frameskips'])

#print(cv2.imread("13.png").shape)

#for i in range(1, 50000):	
#	abc, vid = cap.read()
	#print(np.array(vid))
#	val = m1.predictImage(np.array(vid), returnTensor=True)
#	if i % 25 == 0:
#		print("Iteration: ", i, " is ", val)
#	i += 1

#m1.delModel()
#cap.release()


#We will use predictImage function and pass image from camera class as argument
#i.e camera.GetImage()

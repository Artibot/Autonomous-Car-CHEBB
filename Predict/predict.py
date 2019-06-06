import threading
import numpy as np
import load_graph 
import sys
import os
from keras.models import load_model
from keras import backend as k
import imageCapture as iCap

class Predict:
	model1 = 0
	cap = 0

	def __init__(self, model_name, width = 128, height = 128):


		#model_name = "ResNet_steering_FT_150x2.EP11-0.10-0.13.h5" # Name of the model that is going to be used for predicting images
				# open cam
		args = iCap.parse_args()

		self.cap = iCap.open_cam_usb(args.video_dev, args.image_width, args.image_height)
		if not self.cap.isOpened():
			sys.exit('Failed to open camera!')

		
		# Create an object from MyModel class of #load_graph.py filew
		self.model1 = load_graph.MyModel(width, height, model_name) 

	def __cleansession(self):
		self.model1.delModel()
		self.cap.release()

	def predict_angle(self, st_en):
		dummy, vid = self.cap.read()
		axis = self.model1.predictImage(np.array(vid), True) * st_en # Get steering angle from camera
		axis = np.clip(axis,-5,5)/5
		return axis
		






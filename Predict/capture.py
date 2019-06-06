import numpy as np
import os
import numpy.random as rand
from PIL import Image

import imageCapture as iCap

class Capture:
	cap = 0

	def __init__(self):


		#model_name = "ResNet_steering_FT_150x2.EP11-0.10-0.13.h5" # Name of the model that is going to be used for predicting images
				# open cam
		args = iCap.parse_args()

		self.cap = iCap.open_cam_usb(args.video_dev, args.image_width, args.image_height)
		if not self.cap.isOpened():
			print('Failed to open camera!')


	def __cleansession(self):
		self.cap.release()


	def capture(self, angle, fram):
		__, vid = self.cap.read()
		im = Image.fromarray(np.array(vid))
		if not os.path.exists('/data/'):
			os.mkdir('/data/')		
		filename = '/data/f_{}_{}_s_{}_t_0.jpg'.format(fram, rand.randint(low = 0, high = 9999), angle)
		im.resize((128,128))
		im.save(filename)
		print('saved to filename' + filename)






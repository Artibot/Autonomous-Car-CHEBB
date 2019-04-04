# Sources:
#	https://devblogs.nvidia.com/tensorrt-3-faster-tensorflow-inference/?fbclid=IwAR0Fmj2dgYMo3iDr6irqDVFzRXWjDZikpy5x1-plUEIpegoAaiut8hIv_No


import tensorrt as trt
import uff
from tensorrt.parsers import uffparser
from tensorrt.lite import Engine
from tensorrt.infer import LogSeverity
import imageCapture as iCap


#Model specifics
model_name = "temp.pb"
engine_name = "keras_vgg19_b1_FP32.engine"
input_node_name = "Input_1"
output_node_name = "Output0"
input_width = 128
input_height = 128

#Create logger
G_LOGGER = trt.infer.ConsoleLogger(trt.infer.LogSeverity.INFO)

#Load model
uff_model = uff.from_tensorflow_frozen_model(model_name, [output_node_name])

# Create a UFF parser to parse the UFF file created from your TF Frozen model
parser = uffparser.create_uff_parser()
parser.register_input(input_node_name, (3, input_width, input_height), 0)
parser.register_output(output_node_name)

#Engine
# Build your TensorRT inference engine
# This step performs (1) Tensor fusion (2) Reduced precision 
# (3) Target autotuning (4) Tensor memory management
engine = trt.utils.uff_to_trt_engine(G_LOGGER, 
                                     uff_model,
                                     parser,
                                     1,
                                     1<<20, 
                                     trt.infer.DataType.FLOAT) #FP32 FLOAT, FP16 HALF
									

# Serialize TensorRT engine to a file for when you are ready to deploy your model.
trt.utils.write_engine_to_file(engine_name, 
                               engine.serialize())
							   
# Create a runtime engine from plan file using TensorRT Lite API 
engine_single = Engine(PLAN=engine_name,
                       postprocessors={output_node_name:analyze})


#Image processing
args = iCap.parse_args()
cap = iCap.open_cam_onboard(args.image_width, args.image_height)
if not cap.isOpened():

	sys.exit('Failed to open camera!')


for i in range(0, 1500):
	abc, vid = cap.read()
	#vid = load_and_preprocess_images()
	if vid.shape[0] != input_width:
				if vid.shape[1] != input_height:
					im = cv2.resize(im, (input_width, input_height))
			im = cv2.cvtColor(im, cv2.COLOR_BGR2RGB)
			im = (im.astype('float') / 255.0)
			im = np.array(im)
			im = np.expand_dims(im, axis=0)
	#results = []#for image in images_trt:
	prediction = engine_single.infer(im) # Single function for inference
	print(prediction)

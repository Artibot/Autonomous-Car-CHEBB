#Inference with TensorFlowRT
#   Author: Eivind

#Reference: https://docs.nvidia.com/deeplearning/sdk/tensorrt-developer-guide/index.html#importing_trt_python
    #NOTE: There might be issues with custom layers (i.e from keras) research this link:
    #https://docs.nvidia.com/deeplearning/sdk/tensorrt-developer-guide/index.html#add_custom_layer_python

import tensorflow.contrib.tensorrt as trt
import cv2
import numpy as np

#Convert tensorflow (.pb) graph to .uff for TensorflowRT
#"convert-to-uff" depends on the system path
#Location can be found: python3 -c “import uff; print(uff.__path__)”
#Only need to do once before inferencing
convert-to-uff input_file.pb [-o output_file] [-O output_node]

#Logger for debugging
TRT_LOGGER = trt.Logger(trt.Logger.WARNING)

#Define model name and path
model_file = '/data/mnist/mnist.uff'

#Image processing
image_width = 28
image_height = 28

im = cv2.imread("image_name.png")
im = cv2.resize(im, (image_width, image_height))
im = cv2.cvtColor(im, cv2.COLOR_BGR2RGB)
im = im.astype('float') / 255.0
im = np.array(im)
im = np.expand_dims(im, axis=0)
#use "im" now for input array to model



#Setup model with builder and parser
with builder = trt.Builder(TRT_LOGGER) as builder, builder.create_network() as network, trt.UffParser() as parser:

    #Send image np.array to model's first layer name
    parser.register_input("input_layer_name", im)

    #Output the prediction tensor to model's output name
    parser.register_output("output_layer_name")

    #Determine if this is the output
    parser.parse(model_file, network)


    #Setting up an engine for optimized inferencing:
    #https://docs.nvidia.com/deeplearning/sdk/tensorrt-developer-guide/index.html#build_engine_python
    builder.max_batch_size = max_batch_size
    builder.max_workspace_size = 1 <<  20 # This determines the amount of memory available to the builder when building an optimized engine and should generally be set as high as possible.

# INFERENCE WITH ENGINE! THIS NEEDS TO BE CONFIGURED
with trt.Builder(TRT_LOGGER) as builder:
    with builder.build_cuda_engine(network) as engine:
        # Determine dimensions and create page-locked memory buffers (i.e. won't be swapped to disk) to hold host inputs/outputs.
        h_input = cuda.pagelocked_empty(engine.get_binding_shape(0).volume(), dtype=np.float32)
        h_output = cuda.pagelocked_empty(engine.get_binding_shape(1).volume(), dtype=np.float32)
        # Allocate device memory for inputs and outputs.
        d_input = cuda.mem_alloc(h_input.nbytes)
        d_output = cuda.mem_alloc(h_output.nbytes)
        # Create a stream in which to copy inputs/outputs and run inference.
        stream = cuda.Stream()

        #Hopefully the predicted answer from output
        print(stream)
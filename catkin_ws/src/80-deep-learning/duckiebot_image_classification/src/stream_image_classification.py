#!/usr/bin/python
from cv_bridge import CvBridge, CvBridgeError
from sensor_msgs.msg import CompressedImage, Image
import cv2
import rospy
import threading
import time
import numpy as np
# Movidius NCS related packages
import mvnc.mvncapi as mvnc
import numpy
import os
import sys

# Movidius user modifiable input parameters
NCAPPZOO_PATH           = os.path.expanduser( '~/workspace/ncappzoo' )
GRAPH_PATH              = NCAPPZOO_PATH + '/caffe/GoogLeNet/graph' 
IMAGE_PATH              = NCAPPZOO_PATH + '/data/images/cat.jpg'
LABELS_FILE_PATH        = NCAPPZOO_PATH + '/data/ilsvrc12/synset_words.txt'
IMAGE_MEAN              = [ 104.00698793, 116.66876762, 122.67891434]
IMAGE_STDDEV            = 1
IMAGE_DIM               = ( 224, 224 )

# Look for enumerated NCS device(s); quit program if none found.
devices = mvnc.EnumerateDevices()
if len( devices ) == 0:
    print( 'No devices found' )
    quit()
# Get a handle to the first enumerated device and open it
device = mvnc.Device( devices[0] )
device.OpenDevice()
# ---- Step 2: Load a graph file onto the NCS device -------------------------
# Read the graph file into a buffer
with open( GRAPH_PATH, mode='rb' ) as f:
    blob = f.read()
# Load the graph buffer into the NCS
graph = device.AllocateGraph( blob )





# subscribe to the published compressed images from duckiebot on-board camera
def callback(data):
    rospy.loginfo("I can see the images from duckieCamera!!!")
def listener():
    rospy.init_node('compressed_image_listener', anonymous=True)
    rospy.Subscriber("/tianlu/camera_node/image/compressed", CompressedImage, callback)
    
    
    
    
if __name__ == '__main__':
    # get compressed images from camera
    listener() 
    # ---- Step 3: Offload image onto the NCS to run inference -------------------
    # Read & resize image [Image size is defined during training]
    img = print_img = cv2.imread( IMAGE_PATH )
    img = cv2.resize( img, IMAGE_DIM)
    # Convert RGB to BGR [skimage reads image in RGB, but Caffe uses BGR]
    img = img[:, :, ::-1]
    # Mean subtraction & scaling [A common technique used to center the data]
    img = img.astype( numpy.float32 )
    img = ( img - IMAGE_MEAN ) * IMAGE_STDDEV
    # Load the image as a half-precision floating point array
    graph.LoadTensor( img.astype( numpy.float16 ), 'user object' )
    # ---- Step 4: Read & print inference results from the NCS -------------------
    # Get the results from NCS
    output, userobj = graph.GetResult()
    # Print the results
    print('\n------- predictions --------')
    labels = numpy.loadtxt( LABELS_FILE_PATH, str, delimiter = '\t' )
    order = output.argsort()[::-1][:6]
    for i in range( 0, 4 ):
        print ('prediction ' + str(i) + ' is ' + labels[order[i]])

    # ---- Step 5: Unload the graph and close the device -------------------------
    #graph.DeallocateGraph()
    #device.CloseDevice()
    rospy.spin()    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    

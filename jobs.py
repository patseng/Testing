import cv2
from cv2 import cv
from flask.ext.rq import job
import numpy as np
import urllib
import boto

@job
def process(url):
	# Load image as string from url
	img_str = urllib.urlopen(url).read()

	# convert from a string to a numpy array
	np_arr = np.fromstring(img_str, np.uint8)

	# decode the image from the array
	img_np = cv2.imdecode(np_arr, cv2.CV_LOAD_IMAGE_COLOR)

	# manipulate the image
	img_np = cv2.cvtColor(img_np, cv2.COLOR_BGR2GRAY)
	for _ in xrange(3):
		img_np = cv2.pyrDown(img_np)
	img_np = np.transpose(img_np)

	# encode the image into an array
	retval, encoding = cv2.imencode(".png", img_np)

	# concert the encoding into a string
	img_str = encoding.tostring()

	# connect to s3 and upload the image
	s3 = boto.connect_s3()
	bucket = s3.get_bucket('680bunch')
	destination = bucket.new_key("updated.png")
	print destination.set_contents_from_string(img_str)

	return True
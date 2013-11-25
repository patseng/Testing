import cv2
from cv2 import cv
from flask.ext.rq import job
import numpy as np
import urllib

@job
def process(url):
	# Load image as string from url
	print url
	img_str = urllib.urlopen(url).read()

	# CV2
	nparr = np.fromstring(img_str, np.uint8)
	img_np = cv2.imdecode(nparr, cv2.CV_LOAD_IMAGE_COLOR)

	cv2.imshow('', img_np)
	cv2.waitKey(0)
	cv2.destroyAllWindows()

	# CV
	img_ipl = cv.CreateImageHeader((img_np.shape[1], img_np.shape[0]), cv.IPL_DEPTH_8U, 3)
	cv.SetData(img_ipl, img_np.tostring(), img_np.dtype.itemsize * 3 * img_np.shape[1])

	# check types
	print type(img_str)
	print type(img_np)
	print type(img_ipl)

	return True
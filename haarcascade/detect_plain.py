# import the necessary packages
import argparse
import imutils
import time
#import dlib
import cv2

def convert_and_trim_bb(image, rect):
	# extract the starting and ending (x, y)-coordinates of the
	# bounding box
	startX = rect.left()
	startY = rect.top()
	endX = rect.right()
	endY = rect.bottom()
	# ensure the bounding box coordinates fall within the spatial
	# dimensions of the image
	startX = max(0, startX)
	startY = max(0, startY)
	endX = min(endX, image.shape[1])
	endY = min(endY, image.shape[0])
	# compute the width and height of the bounding box
	w = endX - startX
	h = endY - startY
	# return our bounding box coordinates
	return (startX, startY, w, h)

# construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", type=str, required=True,
	help="path to input image")
ap.add_argument("-m", "--model", type=str,
	default="haarcascade_frontalface_default.xml",
	help="path to OpenCV's Haar Cascade face detector model")
ap.add_argument("-u", "--upsample", type=int, default=1,
	help="# of times to upsample")
args = vars(ap.parse_args())

print("[INFO] loading Haar cascade face detector using {}...".format(args["model"]))
detector = cv2.CascadeClassifier(cv2.data.haarcascades + args["model"])
# load the input image from disk, resize it, and convert it from
# BGR to RGB channel ordering (which is what dlib expects)
image = cv2.imread(args["image"])
#image = imutils.resize(image, width=2000)
#rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
# perform face detection using dlib's face detector
start = time.time()
print("[INFO[ performing face detection with OpenCV...")
boxes = detector.detectMultiScale(image)
end = time.time()
print("[INFO] face detection found {} faces and took {:.4f} seconds".format(len(boxes), end - start))

# loop over the bounding boxes
for (x, y, w, h) in boxes:
    # draw the bounding box on our image
    cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)
    print("detected face at ({},{}) size ({},{})".format(x,y,w,h))

# show the output image
cv2.imwrite('haar_result.jpg', image)
cv2.imshow("Output", image)
cv2.waitKey(0)

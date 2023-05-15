# import the necessary packages
import argparse
import imutils
import time
#import dlib
import cv2
import numpy

# construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", type=str, required=True,
	help="path to occupied input image")

ap.add_argument("-e", "--image_empty", type=str, required=True,
	help="path to empty input image")

ap.add_argument("-b", "--brightness", type=int, required=False, default=0,
	help="brightness value [-127,127]")

args = vars(ap.parse_args())

print("[INFO] loading diff model for {}...".format(args["image"]))

# load the input image from disk, resize it, and convert it from
# BGR to RGB channel ordering (which is what dlib expects)
image = cv2.imread(args["image"])
image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

image_empty = cv2.imread(args["image_empty"])
image_empty_adj = cv2.convertScaleAbs(image_empty, 1, args["brightness"])
image_empty_adj = cv2.cvtColor(image_empty, cv2.COLOR_BGR2HSV)

#cv2.convertScaleAbs(image_empty, contrast 0..1..+ve, brightness [-127, 127])
#cv2.imshow("Empty", image_empty)

# Calculate the per-element absolute difference between
# two arrays or between an array and a scalar
image_diff = cv2.absdiff(image, image_empty_adj)
image_diff = cv2.cvtColor(image_diff, cv2.COLOR_HSV2BGR)
image_diff = cv2.cvtColor(image_diff, cv2.COLOR_BGR2GRAY)

#image = imutils.resize(image, width=2000)
#rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
# perform face detection using dlib's face detector
start = time.time()

print("[INFO[ performing face detection with OpenCV...")
#boxes = detector.detectMultiScale(image)
#end = time.time()
#print("[INFO] face detection found {} faces and took {:.4f} seconds".format(len(boxes), end - start))

# loop over the bounding boxes
#for (x, y, w, h) in boxes:
#    # draw the bounding box on our image
#    cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)
#    print("detected face at ({},{}) size ({},{})".format(x,y,w,h))

# show the output image
#cv2.imwrite('haar_result.jpg', image)
cv2.imshow("Diff", image_diff)
cv2.waitKey(0)
cv2.destroyAllWindows()

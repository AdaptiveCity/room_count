# import the necessary packages
import sys
import topdown
import numpy as np
import argparse
import imutils
import time
import cv2
import cameratransform

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
topdown.add_arguments(ap)
args = ap.parse_args()
argsv = vars(args)

print("[INFO] loading Haar cascade face detector using {}...".format(argsv["model"]))
detector = cv2.CascadeClassifier(cv2.data.haarcascades + argsv["model"])
# load the input image from disk, resize it, and convert it from
# BGR to RGB channel ordering (which is what dlib expects)
image = cv2.imread(argsv["image"])
# perform face detection using dlib's face detector
start = time.time()
print("[INFO] performing face detection with OpenCV...")
boxes = detector.detectMultiScale(image)
end = time.time()
print("[INFO] face detection found {} faces and took {:.4f} seconds".format(len(boxes), end - start))

td = topdown.Topdown(args, (image.shape[1], image.shape[0]), scalefactors=5)
if not td.ready():
        print('Topdown failed to initialise: {}'.format(td.errormsg))
        sys.exit(1)

bottomCentres = []

# loop over the bounding boxes
for (x, y, w, h) in boxes:
        # draw the bounding box on our image
        cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)
        bottomCentre = (x+w/2, y+h)
        bottomCentres.append(bottomCentre)

#print(bottomCentres)
tdCoords = td.topdownFromImage(bottomCentres) + np.array([310,0])
#print(tdCoords)
topdown_image = np.zeros((480,640,3),dtype=np.uint8)
for tdCoord in tdCoords:
        cv2.circle(topdown_image, (int(tdCoord[0]), int(tdCoord[1])), 2, (0, 255, 0), -1)

# show the output image
cv2.imwrite('haar_result.jpg', image)
cv2.imwrite('topdown.jpg', topdown_image)
cv2.imwrite('camtopview.jpg', td.getTopViewofImage(image))
# cv2.imshow("Output", image)
# cv2.waitKey(0)

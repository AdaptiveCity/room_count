from __future__ import print_function
import cv2 as cv
import argparse
import numpy as np

parser = argparse.ArgumentParser(description='This program shows how to use background subtraction methods provided by \
                                              OpenCV. You can process both videos and images.')
parser.add_argument('--input', type=str, help='Path to a video or a sequence of image.', default='videos/vtest.avi')
parser.add_argument('--algo', type=str, help='Background subtraction method (KNN, MOG2).', default='MOG2')
args = parser.parse_args()

## [create]
#create Background Subtractor objects
if args.algo == 'MOG2':
    backSub = cv.createBackgroundSubtractorMOG2()
else:
    backSub = cv.createBackgroundSubtractorKNN()
## [create]

## [capture]
#capture = cv.VideoCapture(cv.samples.findFileOrKeep(args.input))
capture = cv.VideoCapture(0)

if not capture.isOpened():
    print('Unable to open: ' + args.input)
    exit(0)
## [capture]

while True:
    ret, frame = capture.read()
    if frame is None:
        break

    ## [apply]
    #update the background model
    fgMask = backSub.apply(frame)
    ## [apply]

    ## [display_frame_number]
    #get the frame number and write it on the current frame
    cv.rectangle(frame, (10, 2), (100,20), (255,255,255), -1)
    cv.putText(frame, str(capture.get(cv.CAP_PROP_POS_FRAMES)), (15, 15),
               cv.FONT_HERSHEY_SIMPLEX, 0.5 , (0,0,0))
    ## [display_frame_number]

    kernel1 = cv.getStructuringElement(cv.MORPH_ELLIPSE,(7,7))
    kernel2 = np.ones((5,5),np.uint8)
    erosion = cv.erode(fgMask,kernel2,iterations = 1)
    dilation = cv.dilate(erosion,kernel1,iterations = 7)

    ## [show]
    #show the current frame and the fg masks
    cv.imshow('Frame', frame)
    cv.imshow('FG Mask', fgMask)
    cv.imshow('Dilation', dilation)
    ## [show]

    keyboard = cv.waitKey(30)
    if keyboard == 'q' or keyboard == 27:
        break

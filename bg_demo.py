from __future__ import print_function
import cv2 as cv
import argparse
import numpy as np

parser = argparse.ArgumentParser(description='This program shows how to use background subtraction methods provided by \
                                              OpenCV. You can process both videos and images.')
parser.add_argument('--input', type=str, help='Path to a video or a sequence of image.', default='')
parser.add_argument('--algo', type=str, help='Background subtraction method (KNN, MOG2).', default='MOG2')
parser.add_argument('--rate', type=str, help='Background learning rate, e.g. 0.1', default='-1')
args = parser.parse_args()

## [create]
#create Background Subtractor objects
if args.algo == 'MOG2':
    backSub = cv.createBackgroundSubtractorMOG2()
else:
    backSub = cv.createBackgroundSubtractorKNN()
## [create]

bs_rate = float(args.rate)

capture = None
frame_number = 0

def init_video():
    global capture, frame_number
    ## [capture]
    if args.input == '':
        capture = cv.VideoCapture(0)
    else:
        capture = cv.VideoCapture(cv.samples.findFileOrKeep(args.input))
    if not capture.isOpened():
        print('Unable to open: ' + args.input)
        exit(0)
    frame_number = 0


pause = True

init_video()

while True:
    keyboard = cv.waitKey(30)
    if keyboard == ord('q') or keyboard == 27:
        print("Keyboard quit")
        break
    elif keyboard == ord('p') or keyboard == ord(' '):
        pause = not pause
        print("Toggle pause to "+str(pause))
    elif keyboard == ord('<') and args.input != '':
        print("Restarting video")
        init_video()

    if pause and frame_number != 0:
        continue

    frame_number += 1

    ret, frame = capture.read()
    if frame is None:
        pause = True
        init_video()
        continue

    ## [apply]
    #update the background model
    fgMask = backSub.apply(frame,learningRate=bs_rate)
    ## [apply]

    ## [display_frame_number]
    #get the frame number and write it on the current frame
    cv.rectangle(frame, (10, 2), (100,20), (255,255,255), -1)
    cv.putText(frame, str(capture.get(cv.CAP_PROP_POS_FRAMES)), (15, 15),
               cv.FONT_HERSHEY_SIMPLEX, 0.5 , (0,0,0))
    ## [display_frame_number]

    erosion_kernel = np.ones((7,7),np.uint8)
    erosion_img = cv.erode(fgMask,erosion_kernel,iterations = 1)

    dilation_kernel = cv.getStructuringElement(cv.MORPH_ELLIPSE,(3,3))
    dilation_img = cv.dilate(erosion_img,dilation_kernel,iterations = 7)

    ## [show]
    #show the current frame and the fg masks
    cv.imshow('Frame', frame)
    cv.imshow('FG Mask', fgMask)
    cv.imshow('erosion', erosion_img)
    cv.imshow('Dilation', dilation_img)
    ## [show]


from __future__ import print_function
import cv2
import argparse
import numpy as np

parser = argparse.ArgumentParser(description='An image pipeline to count a seated room audience')
parser.add_argument('--input', type=str, help='Path to a video or a sequence of image.', default='')
parser.add_argument('--algo', type=str, help='Background subtraction method (KNN, MOG2).', default='MOG2')
parser.add_argument('--rate', type=str, help='Background learning rate, e.g. 0.1', default='-1')
args = parser.parse_args()

## [create]
#create Background Subtractor objects
if args.algo == 'MOG2':
    subtractor = cv2.createBackgroundSubtractorMOG2()
    subtractor.setShadowValue(0)
else:
    subtractor = cv2.createBackgroundSubtractorKNN()
## [create]

bs_rate = float(args.rate)

erosion_kernel = np.ones((11,11),np.uint8)
dilation_kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(3,3))

# Min perspetive box area for a seated person
box_area_min = 2500

# Build perspective matrix
# Input image size
frame_w = 848
frame_h = 480
# specify desired output size
p_w = 1200
p_h = 1000

# specify conjugate x,y coordinates (not y,x)
# points top-left, top-right, bottom-right, bottom-left
in_coords = np.float32([[0, 0], [frame_w,0], [frame_w ,frame_h], [0,frame_h]])
out_coords = np.float32([[-1000,-1200], [2300,-1200], [800,1200], [550,1200]])

# compute perspective matrix
p_matrix = cv2.getPerspectiveTransform(in_coords,out_coords)
p_matrix_inv = np.linalg.pinv(p_matrix)

# Perspective image
img_p = np.zeros((p_w, p_h), dtype=np.uint8)

# Iterate through images
capture = None
frame_number = 0

def init_video():
    global capture, frame_number
    ## [capture]
    if args.input == '':
        capture = cv2.VideoCapture(0)
    else:
        capture = cv2.VideoCapture(cv2.samples.findFileOrKeep(args.input))
    if not capture.isOpened():
        print('Unable to open: ' + args.input)
        exit(0)
    frame_number = 0

seating_mask_input = cv2.imread("images/LT1_mask.jpg")
seating_mask_gray = cv2.cvtColor(seating_mask_input, cv2.COLOR_BGR2GRAY)
(thresh, seating_mask) = cv2.threshold(seating_mask_gray, 127, 255, cv2.THRESH_BINARY)

pause = True

init_video()

while True:
    keyboard = cv2.waitKey(30)
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

    #print("frame.shape="+str(frame.shape))
    ## [apply]
    #update the background model
    img_fg = subtractor.apply(frame,learningRate=bs_rate)

    img_fg_masked = cv2.bitwise_and(img_fg, img_fg, mask=seating_mask)

    img_p[0:frame_h,0:frame_w] = img_fg_masked

    # do perspective transformation setting area outside input to black
    img_iso = cv2.warpPerspective(img_p, p_matrix, (p_w,p_h), cv2.INTER_LINEAR, borderMode=cv2.BORDER_CONSTANT, borderValue=(0,0,0))

    img_color_iso = cv2.cvtColor(img_iso,cv2.COLOR_GRAY2RGB)

    #print("img_iso shape "+str(img_iso.shape))

    img_erosion = cv2.erode(img_iso,erosion_kernel,iterations = 3)

    img_dilation = cv2.dilate(img_erosion,dilation_kernel,iterations = 7)

    # bounding boxes
    contours, hierarchy  = cv2.findContours(img_dilation, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    #cv2.drawContours(img_iso, contours, -1, (0,255,75), 2)
    #print(str(len(contours)) + " contours")

    # Draw a bounding box around all contours
    for c in contours:
        # Make sure contour area is large enough
        if (cv2.contourArea(c)) > box_area_min:
            x, y, w, h = cv2.boundingRect(c)
            cv2.rectangle(img_color_iso, (x,y), (x+w,y+h), (255,255,0), 5)

    #img_boxes = cv2.perspectiveTransform(img_iso, p_matrix_inv)

    ## [show]
    #show the current frame and the fg masks
    ## [display_frame_number]
    #get the frame number and write it on the current frame
    cv2.rectangle(frame, (10, 2), (100,20), (255,255,255), -1)
    cv2.putText(frame, str(capture.get(cv2.CAP_PROP_POS_FRAMES)), (15, 15),
               cv2.FONT_HERSHEY_SIMPLEX, 0.5 , (0,0,0))
    cv2.imshow('Frame', frame)

    cv2.imshow('FG Mask', img_fg)
    cv2.imshow('erosion', img_erosion)
    cv2.imshow('Dilation', img_dilation)
    cv2.imshow('ISO', img_color_iso)
    ## [show]

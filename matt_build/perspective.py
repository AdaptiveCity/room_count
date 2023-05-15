import numpy as np
import cv2 as cv

# specify desired output size
p_w = 1200
p_h = 1000
img_p = np.zeros((p_w, p_h,  3), dtype=np.uint8)

# read input
frame = cv.imread("images/LT1.jpg")
frame_w = frame.shape[1]
frame_h = frame.shape[0]
img_p[0:frame_h,0:frame_w] = frame

cv.imshow("Larger", img_p)


# specify conjugate x,y coordinates (not y,x)
# points top-left, top-right, bottom-right, bottom-left
in_coords = np.float32([[0, 0], [frame_w,0], [frame_w ,frame_h], [0,frame_h]])
out_coords = np.float32([[-1000,-1200], [2300,-1200], [800,1200], [550,1200]])

# compute perspective matrix
matrix = cv.getPerspectiveTransform(in_coords,out_coords)

print(matrix.shape)
print(matrix)

# do perspective transformation setting area outside input to black
img_iso = cv.warpPerspective(img_p, matrix, (p_w,p_h), cv.INTER_LINEAR, borderMode=cv.BORDER_CONSTANT, borderValue=(0,0,0))
print(img_iso.shape)

# save the warped output
#cv.imwrite("sudoku_warped.jpg", imgOutput)

# show the result
cv.imshow("result", img_iso)
cv.waitKey(0)
cv.destroyAllWindows()

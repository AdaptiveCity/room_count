import numpy as np
import cv2

img_in_larger_size = { "w": 1200, "h": 1000 }
img_in_larger = np.zeros((img_in_larger_size["w"], img_in_larger_size["h"],3), dtype=np.uint8)

img_in_size = {"w": 848, "h": 480}

# read input
img_in = cv2.imread("images/LT1.jpg")

x_offset = 30
y_offset = 0
x_end = x_offset + img_in.shape[1]
y_end = y_offset + img_in.shape[0]
img_in_larger[y_offset:y_end,x_offset:x_end] = img_in

cv2.imshow("Larger", img_in_larger)

# specify desired output size
width = 1200
height = 1000

# specify conjugate x,y coordinates (not y,x)
# points top-left, top-right, bottom-right, bottom-left
input = np.float32([[x_offset, y_offset],
                    [x_offset+img_in_size["w"],y_offset],
                    [x_offset+img_in_size["w"],y_offset+img_in_size["h"]],
                    [x_offset,y_offset+img_in_size["h"]]])
output = np.float32([[-1000,-1200], [2300,-1200], [800,1200], [550,1200]])

# compute perspective matrix
matrix = cv2.getPerspectiveTransform(input,output)

print(matrix.shape)
print(matrix)

# do perspective transformation setting area outside input to black
img_iso = cv2.warpPerspective(img_in_larger, matrix, (width,height), cv2.INTER_LINEAR, borderMode=cv2.BORDER_CONSTANT, borderValue=(0,0,0))
print(img_iso.shape)

# save the warped output
#cv2.imwrite("sudoku_warped.jpg", imgOutput)

# show the result
cv2.imshow("result", img_iso)
cv2.waitKey(0)
cv2.destroyAllWindows()

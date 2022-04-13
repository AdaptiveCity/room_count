# dlib MMOD CNN face detection

https://pyimagesearch.com/2021/04/19/face-detection-with-dlib-hog-and-cnn/

## Test run
```
$ python cnn_face_detection.py --image images/concert.jpg
[INFO] loading CNN face detector...
[INFO[ performing face detection with dlib...
[INFO] face detection took 2.2520 seconds
```

## Lecture Theatre

Model `mmod_human_face_detector.dat` using `imutils.resize(image, width=2000)`:

### Source image
![pre detect](../images/ADFA_Lecture_Theatres.jpg)

### After detect run, 18 seconds on non-GPU PC

![post detect](../images/ADFA_Lecture_Theatres_detect.jpg)

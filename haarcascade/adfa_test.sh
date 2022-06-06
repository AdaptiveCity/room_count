#!/bin/bash

IMG="ADFA_Lecture_Theatres.jpg"

python3 haar_face_detection.py --3d \
	--sensor-width-mm 6.7 --sensor-height-mm 5.6 --focallength-mm 7.0 \
	--pos-x-m 0 --pos-y-m 0 --elevation-m 1.8 \
	--tilt-deg 76 --heading-deg 0 --roll-deg 0  --image "$IMG" $@

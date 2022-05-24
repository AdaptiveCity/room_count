#!/bin/bash
source ../venv/bin/activate
eog ../images/ADFA_Lecture_Theatres.jpg &
python haar_face_detection.py --image ../images/ADFA_Lecture_Theatres.jpg

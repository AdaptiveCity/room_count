#!/bin/bash
source ../venv/bin/activate
eog test.jpg &
python cnn_face_detection.py --image test.jpg

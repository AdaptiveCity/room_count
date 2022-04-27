# Room occupancy people counting in Python

```
git clone https://github.com/AdaptiveCity/room_count

cd room_count
python3 -m venv venv
source venv/bin/activate
python3 -m pip install pip --upgrade
python3 -m pip install wheel
```
On Intel x64/Ubuntu:
```
python -m pip install opencv-contrib-python
```

On Raspian, see [Pi opencv install instructions](pi_opencv.md).

This repo is a work-in-progress. To run the sample program:
```
python3 bg_demo.py --input videos/LT1_01.webm --rate 0
```

To run the program using the camera as input omit the `--input` parameter.


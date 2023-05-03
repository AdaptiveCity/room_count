# Room occupancy people counting in Python

## Updating camera library - 2023 May version  
### More information found below  
https://www.raspberrypi.com/documentation/computers/camera_software.html
https://datasheets.raspberrypi.com/camera/picamera2-manual.pdf

## Faster OpenCV installation on Raspberry Pi 4B - 2023 May version
### More information found below  
https://pypi.org/project/opencv-python/

## Install on x86(-64) - 2022 August version  

```
# On Debian-based systems for OpenCV support:
apt-get install -y libatlas-base-dev libavcodec58 libavformat58 libswscale5

# Then:
pip install -r requirements.txt
```


## Install on ARMv7 (e.g. Raspberry Pi 4B) - 2022 August version  

```
# On Debian-based systems for OpenCV support:
apt-get install -y libatlas-base-dev libavcodec58 libavformat58 libswscale5
pip install -r rpi-armv7-requirements.txt
```

### Docker alternative - 2022 August version  

Edit a file named `local_settings` and set an environment variable `RPI_DOCKER_IMAGE` with the name of a target docker image if you like. Then,

```
./rpi-armv7-build.sh
```

Push the image and pull it onto the Raspberry Pi using the Docker hub or however you like.

On the Pi, you can use `rpi-armv7-run.sh` as a convenient script to run a command inside of the container, or as an example for your own scripts.

## Running it

```
python3 dump_face_detections.py [options] <image_file>*
```

For each input image file, unless `-d` is specified, it outputs JSON to stdout comprising a list of entries with `confidence` scores, `x`, `y`, `w` and `h` boxes in pixel coordinates.
When `--verbose` is given as an option, the output instead includes `n_results` counting the number of faces found in the image and `detections` having the list as specified above. 

Optional arguments:

- `--score-threshold`, giving the minimum confidence threshold, defaulting to 0.7.
- `--backend`, currently allowable options are `yunet` (default) or `mtcnn` (must install `mtcnn` python package).
- `--default-output` or `-d`, for each input image file, write JSON output to `<image_file>.det`, replacing the JPG extension with `.det`.
- `--verbose`, output to stdout as described above; if `-d` is specified then JSON output also goes to the files as usual.

### Example:

```
python3 dump_face_detections.py --score-threshold 0.8 -d images-*.jpg
```

This changes the score threshold to 0.8 (80%) and outputs JSON into files matching `images-*.det`.


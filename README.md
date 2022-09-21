# Room occupancy people counting in Python

## Install on x86(-64)

```
# On Debian-based systems for OpenCV support:
apt-get install -y libatlas-base-dev libavcodec58 libavformat58 libswscale5

# Then:
pip install -r requirements.txt
```


## Install on ARMv7 (e.g. Raspberry Pi 4B)

```
# On Debian-based systems for OpenCV support:
apt-get install -y libatlas-base-dev libavcodec58 libavformat58 libswscale5
pip install -r rpi-armv7-requirements.txt
```

### Docker alternative

Edit a file named `local_settings` and set an environment variable `RPI_DOCKER_IMAGE` with the name of a target docker image if you like. Then,

```
./rpi-armv7-build.sh
```

Push the image and pull it onto the Raspberry Pi using the Docker hub or however you like.

On the Pi, you can use `rpi-armv7-run.sh` as a convenient script to run a command inside of the container, or as an example for your own scripts.

## Running it

```
python3 dump_face_detections.py [options] <image_file>
```

Outputs JSON to stdout with `n_results` counting the number of faces found in the image and `detections` comprising a list of entries with `confidence` scores, `x`, `y`, `w` and `h` boxes in pixel coordinates.

Optional arguments:

- `--score-threshold`, giving the minimum confidence threshold, defaulting to 0.7.
- `--backend`, currently allowable options are `yunet` (default) or `mtcnn` (must install `mtcnn` python package).


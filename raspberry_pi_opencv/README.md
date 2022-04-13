# OpenCV install on Raspberry Pi (Nov 2021)

Mostly credit https://core-electronics.com.au/tutorials/face-identify-raspberry-pi.html

This takes about 1.5 hours on a RPi4.

## Make Python3 the default (WTF?)
```
sudo update-alternatives --install $(which python) python $(readlink -f $(which python3)) 3
```
Check with:
```
python --version
pip --version
```

## Install pre-reqs

Now is a good time to install your preferred editor e.g. `sudo apt install vim`

```
pip install picamera[array]
sudo apt install cmake build-essential pkg-config git
sudo apt install libjpeg-dev libtiff-dev libjasper-dev libpng-dev libwebp-dev libopenexr-dev
sudo apt install libavcodec-dev libavformat-dev libswscale-dev libv4l-dev libxvidcore-dev libx264-dev libdc1394-22-dev libgstreamer-plugins-base1.0-dev libgstreamer1.0-dev
sudo apt install libgtk-3-dev libqtgui4 libqtwebkit4 libqt4-test python3-pyqt5
sudo apt install libatlas-base-dev liblapacke-dev gfortran
sudo apt install libhdf5-dev libhdf5-103
sudo apt install python3-dev python3-pip python3-numpy
```

## Expand the swap file to 2GB

Check current swap file `CONF_SWAPSIZE` settings with:
```
cat /etc/dphys-swapfile
```

Check size of SD card:
```
df -h
```

Disable current swap:
```
sudo dphys-swapfile swapoff
```

Edit the `/etc/dphys-swapfile` config and set `CONF_SWAPSIZE=2048` e.g.
```
sudo vim /etc/dphys-swapfile
```
Re-init swap:
```
sudo dphys-swapfile setup
sudo dphys-swapfile swapon
sudo reboot
```

## Now build OpenCV
```
git clone https://github.com/opencv/opencv.git
git clone https://github.com/opencv/opencv_contrib.git
mkdir ~/opencv/build
cd ~/opencv/build
cmake -D CMAKE_BUILD_TYPE=RELEASE \
-D CMAKE_INSTALL_PREFIX=/usr/local \
-D OPENCV_EXTRA_MODULES_PATH=~/opencv_contrib/modules \
-D ENABLE_NEON=ON \
-D ENABLE_VFPV3=ON \
-D BUILD_TESTS=OFF \
-D INSTALL_PYTHON_EXAMPLES=OFF \
-D OPENCV_ENABLE_NONFREE=ON \
-D CMAKE_SHARED_LINKER_FLAGS=-latomic \
-D BUILD_EXAMPLES=OFF ..
```
*Alternatively* as one line for easier cut-and-paste, that `cmake` command is:
```
cmake -D CMAKE_BUILD_TYPE=RELEASE -D CMAKE_INSTALL_PREFIX=/usr/local -D OPENCV_EXTRA_MODULES_PATH=~/opencv_contrib/modules -D ENABLE_NEON=ON -D ENABLE_VFPV3=ON -D BUILD_TESTS=OFF -D INSTALL_PYTHON_EXAMPLES=OFF -D OPENCV_ENABLE_NONFREE=ON -D CMAKE_SHARED_LINKER_FLAGS=-latomic -D BUILD_EXAMPLES=OFF ..
```
Here's the lengthy past (~1 hour 10mins):
```
make -j$(nproc)
```
Then:
```
sudo make install
```

## Test in python:

```
import cv2 as cv
```

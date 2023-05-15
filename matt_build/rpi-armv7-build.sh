#!/bin/bash

[ -f 'local_settings' ] && source local_settings

IMAGE="${RPI_DOCKER_IMAGE:-roomcount-rpi-armv7}"

docker build -t "$IMAGE" \
  -f Dockerfile.rpi-armv7 \
  --build-arg USER_ID=1000 \
  --build-arg GROUP_ID=1000 \
  .

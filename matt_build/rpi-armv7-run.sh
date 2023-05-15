#!/bin/bash

[ -f 'local_settings' ] && source local_settings

IMAGE="${RPI_DOCKER_IMAGE:-roomcount-rpi-armv7}"

docker run -it --rm -v "$PWD":/work "$IMAGE" "$@"

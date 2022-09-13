#!/bin/bash

docker run --net=host --privileged -it --rm -v /store:/work mrdanish/motioneye-rpi motion -c motion/motion.conf -d motion/motion.pid -l motion/motion.log -m


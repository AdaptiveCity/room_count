#!/bin/bash

DEFAULTCAM=lt1-rpi4

TIMESPEC="${1:-yesterday}"
CAM="${2:-$DEFAULTCAM}"
DIR="${3:-/store}"
REMOTE="${4:-tfc}"

cd "$DIR"

DATE=`date -Idate -d "$TIMESPEC" | sed -e 's/-//g'`

ssh "$REMOTE" mkdir -p "$CAM/$DATE"
rsync --ignore-errors "$CAM"-$DATE-*jpg "$REMOTE":"$CAM/$DATE"



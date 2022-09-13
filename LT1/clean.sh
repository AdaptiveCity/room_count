#!/bin/bash

DEFAULTCAM=lt1-rpi4

TIMESPEC="${1:-yesterday}"
CAM="${2:-$DEFAULTCAM}"
DIR="${3:-/store}"
REMOTE="${4:-tfc}"

cd "$DIR"

DATE=`date -Idate -d "$TIMESPEC" | sed -e 's/-//g'`

# test if files exist locally
test -n "`compgen -G $CAM-$DATE-*`" || exit 0
# test if dir exists remotely
ssh "$REMOTE" test -d "$CAM/$DATE" || exit 0
# test if all files were copied
files=`rsync -nv --size-only --ignore-errors "$CAM"-$DATE-*jpg "$REMOTE":"$CAM/$DATE" | grep 'jpg' | head`
[ -z "$files" ] && rm -f "$CAM-$DATE"*jpg

#!/usr/bin/env bash

DIRECTORY=$1
if [ ! -d "$DIRECTORY" ]; then
  echo "Directory '${DIRECTORY}' doesn't exist. Aborting'"
  exit 1
fi

image_tag="cig2017_`basename $DIRECTORY`"
container_name=${image_tag}


if [ "`uname`" != "Linux" ]; then
  echo "WARNING: GUI forwarding in Docker was tested only on a linux host."
fi

docker  run -p 5029 --net=host -ti --rm --name ${container_name} \
    -e DISPLAY=${DISPLAY}  ${image_tag} "${@:2}"
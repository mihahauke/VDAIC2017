#!/usr/bin/env bash

DIRECTORY=$1
if [ ! -d "$DIRECTORY" ]; then
  echo "Directory '${DIRECTORY}' doesn't exist. Aborting'"
  exit 1
fi

image_tag="cig2017_`basename $DIRECTORY`"
container_name=${image_tag}

docker  run -p 5029 --net=host -t --rm --name ${container_name} \
    -e DISPLAY=${DISPLAY}  ${image_tag} "${@:2}"
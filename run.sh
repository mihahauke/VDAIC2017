#!/usr/bin/env bash

ERROR_PREFIX="ERROR:"
if [[ ! -z  `which nvidia-docker`  ]]
then
    DOCKER_CMD=nvidia-docker
elif [[ ! -z  `which docker`  ]]
then
    echo "WARNING: nvidia-docker not found. Nvidia drivers may not work." >&2
    DOCKER_CMD=docker
else
     echo "${ERROR_PREFIX} docker or nvidia-docker not found. Aborting." >&2
    exit 1
fi



DIRECTORY=$1
if [ ! -d "$DIRECTORY" ]; then
  echo "${ERROR_PREFIX} Directory '${DIRECTORY}' doesn't exist. Aborting'" >&2
  exit 2
fi

image_tag="cig2017_`basename $DIRECTORY`"
container_name=${image_tag}


if [ "`uname`" != "Linux" ]; then
  echo "WARNING: GUI forwarding in Docker was tested only on a linux host."
fi

$DOCKER_CMD run --net=host -ti --rm --name ${container_name} \
    --env="DISPLAY" --privileged \
    ${image_tag} "${@:2}"

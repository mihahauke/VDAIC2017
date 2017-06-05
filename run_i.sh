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
  echo "${ERROR_PREFIX} Directory '${DIRECTORY}' doesn't exist. Aborting." >&2
  exit 2
fi

image_tag="cig2017_`basename $DIRECTORY`"
container_name=${image_tag}

run_version=0
while [[ ! -z `docker ps --format '{{.Names}}'|grep "^${container_name}$"`  ]]
do
    echo "WARNING: '${container_name}' is already a running docker container. Trying to run '${image_tag}_${run_version}'."
    run_version=$(($run_version+1))
    container_name=${image_tag}_${run_version}
done


if [ "`uname`" != "Linux" ]; then
  echo "WARNING: GUI forwarding in Docker was tested only on a linux host."
fi

$DOCKER_CMD run --net=host -ti --name ${container_name} \
    --env="DISPLAY" --privileged \
    --entrypoint /bin/bash \
    ${image_tag}
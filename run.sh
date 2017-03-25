#!/usr/bin/env bash

docker  run -p 5029 --net=host -t --rm --name ${container_name} \
    -e DISPLAY=${DISPLAY}  ${image_tag} "${@:2}"
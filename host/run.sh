#!/usr/bin/env bash

sudo docker  run -p 5029 --net=host -t --rm --name cig2017_host \
-e DISPLAY=$DISPLAY  cig2017_host "$@"


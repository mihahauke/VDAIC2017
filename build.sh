#!/usr/bin/env bash

DIRECTORY=$1
if [ ! -d "$DIRECTORY" ]; then
  echo "Directory '${DIRECTORY}' doesn't exist. Aborting'"
  exit 1
fi

echo "Entering directory: ${DIRECTORY}"
cd $DIRECTORY

if [ ! -f Dockerfile ]; then
  echo "No Dockerfile found. Aborting.'"
  exit 2
fi

image_tag="cig2017_`basename $DIRECTORY`"
container_name=${image_tag}

if [ ! -f ../cig2017.wad ]; then
  echo "cig2017.wad not found. Aborting."
  exit 3
fi
if [ ! -f ../_vizdoom.cfg ]; then
  echo "_vizdoom.cfg not found. Aborting."
  exit 4
fi

cp ../cig2017.wad .
cp ../_vizdoom.cfg .
if [ -f ../doom2.wad ]; then
  cp ../doom2.wad .
fi

docker build -t ${image_tag} .
rm -f cig2017.wad _vizdoom.cfg doom2.wad


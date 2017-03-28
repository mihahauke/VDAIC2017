#!/usr/bin/env bash

ERROR_PREFIX="ERROR:"
DIRECTORY=$1
REPO_ROOT=`pwd`

# TODO add usage and error that no arguments specified
if [ ! -d "$DIRECTORY" ]; then
  echo "${ERROR_PREFIX} Directory '${DIRECTORY}' doesn't exist. Aborting'" >&2
  exit 1
fi

echo "Entering directory: ${DIRECTORY}"
cd $DIRECTORY

if [ ! -f Dockerfile ]; then
  echo "${ERROR_PREFIX} No Dockerfile found. Aborting." >&2
  exit 2
fi

image_tag="cig2017_`basename $DIRECTORY`"
container_name=${image_tag}

if [ ! -f ${REPO_ROOT}/cig2017.wad ]; then
  echo "${ERROR_PREFIX} cig2017.wad not found. Aborting." >&2
  exit 3
fi
if [ ! -f ${REPO_ROOT}/_vizdoom.cfg ]; then
  echo "${ERROR_PREFIX} _vizdoom.cfg not found. Aborting." >&2
  exit 4
fi

echo ${REPO_ROOT}
cp ${REPO_ROOT}/cig2017.wad .
cp ${REPO_ROOT}/_vizdoom.cfg .
if [ -f ${REPO_ROOT}/doom2.wad ]; then
  cp ${REPO_ROOT}/doom2.wad .
fi

docker build -t ${image_tag} .
rm -f cig2017.wad _vizdoom.cfg doom2.wad


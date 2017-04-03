FROM ubuntu:16.04

# Cuda 7.5 with cudnn 4.0.7
FROM nvidia/cuda:7.5-devel

RUN echo "deb http://developer.download.nvidia.com/compute/machine-learning/repos/ubuntu1404/x86_64 /" > /etc/apt/sources.list.d/nvidia-ml.list
ENV CUDNN_VERSION 4
RUN apt-get update && apt-get install -y --no-install-recommends \
            libcudnn4=4.0.7 libcudnn4-dev=4.0.7

# ViZdoom dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    bzip2 \
    cmake \
    curl \
    git \
    libboost-all-dev \
    libbz2-dev \
    libfluidsynth-dev \
    libfreetype6-dev \
    libgme-dev \
    libgtk2.0-dev \
    libjpeg-dev \
    libopenal-dev \
    libpng12-dev \
    libsdl2-dev \
    libwildmidi-dev \
    libzmq3-dev \
    nano \
    nasm \
    pkg-config \
    rsync \
    software-properties-common \
    sudo \
    tar \
    timidity \
    unzip \
    wget \
    zlib1g-dev

RUN apt-get update && apt-get install -y dbus



# Python with pip
RUN apt-get update && apt-get install -y python-dev python python-pip
RUN pip install pip --upgrade




# Vizdoom and other pip packages if needed
RUN pip --no-cache-dir install \
    git+https://github.com/mwydmuch/ViZDoom

RUN pip --no-cache-dir install \
    https://storage.googleapis.com/tensorflow/linux/gpu/tensorflow-0.9.0-cp27-none-linux_x86_64.whl
RUN pip --no-cache-dir install opencv-python termcolor tqdm subprocess32 msgpack-python msgpack-numpy


# Enables X11 sharing and creates user home directory
ENV USER_NAME cig2017
ENV HOME_DIR /home/$USER_NAME

# Replace HOST_UID/HOST_GUID with your user / group id (needed for X11)
ENV HOST_UID 1000
ENV HOST_GID 1000

RUN export uid=${HOST_UID} gid=${HOST_GID} && \
    mkdir -p ${HOME_DIR} && \
    echo "$USER_NAME:x:${uid}:${gid}:$USER_NAME,,,:$HOME_DIR:/bin/bash" >> /etc/passwd && \
    echo "$USER_NAME:x:${uid}:" >> /etc/group && \
    echo "$USER_NAME ALL=(ALL) NOPASSWD: ALL" > /etc/sudoers.d/$USER_NAME && \
    chmod 0440 /etc/sudoers.d/$USER_NAME && \
    chown ${uid}:${gid} -R ${HOME_DIR}

USER ${USER_NAME}
WORKDIR ${HOME_DIR}


# Copy agent files inside Docker image:
COPY IntelAct_track2 .


### Do not change this ###
COPY cig2017.wad .
COPY _vizdoom.cfg .
##########################
RUN sudo chown ${HOST_UID}:${HOST_GID} -R *


CMD taskset -c 1 python run_agent.py

FROM ubuntu:16.04

# Cuda 7.5 with cudnn 5
#FROM nvidia/cuda:7.5-cudnn5-devel
# Cuda 8 with cudnn 5
FROM nvidia/cuda:8.0-cudnn5-devel

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
    zlib1g-dev \
    python3-dev \
    python3 \
    python3-pip



# Python with pip
#RUN apt-get install -y python-dev python python-pip
#RUN pip install pip --upgrade

# Python3 with pip3
RUN pip3 install pip --upgrade



# Vizdoom and other pip packages if needed
#RUN pip --no-cache-dir install \
#         git+https://github.com/mwydmuch/ViZDoom \
#         numpy \
#RUN pip --no-cache-dir install \
#    https://storage.googleapis.com/tensorflow/linux/gpu/tensorflow-0.10.0-cp27-none-linux_x86_64.whl


# Vizdoom and other pip3 packages if needed
RUN pip3 --no-cache-dir install \
         git+https://github.com/mwydmuch/ViZDoom \
         opencv-python

RUN pip3 --no-cache-dir install \
    https://storage.googleapis.com/tensorflow/linux/gpu/tensorflow_gpu-1.0.1-cp35-cp35m-linux_x86_64.whl


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
COPY config config
COPY sample_random_agent.py .


### Do not change this ###
COPY cig2017.wad .
COPY _vizdoom.cfg .
##########################
# Uncomment to use doom2.wad:
#COPY doom2.wad /usr/local/lib/python3.5/dist-packages/vizdoom

CMD ./sample_random_agent.py

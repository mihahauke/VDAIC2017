
# Sample and Historical submissions for [Visual Doom AI Competition 2017 at CIG2017](http://vizdoom.cs.put.edu.pl/competition-cig-2017)
![doom_logo](https://upload.wikimedia.org/wikipedia/it/d/dd/Logo_doom.png)
>> Submissions require [Docker](https://www.docker.com/). All images except for the host require quite recent Nvidia drivers and [nvidia-docker](https://github.com/NVIDIA/nvidia-docker) to run CUDA.

>>> GUI forwarding from Docker was tested only on a Linux host and it's not guaranteed to work properly on other systems at the moment.

## Quick Start
```
./build.sh host
./build.sh random
./run.sh host -w
./run.sh random  # in a different terminal
```

## Building and Running the Images
We have prepared two wrapper scripts which will [build](build.sh) and [run](run.sh) docker images with agents and the [host](host).

>>> To run gui on X11 properly make sure that GID and UID are the same in Dockerfile as in your host.

To build and launch given container run:
```
DIR=host # or any other directory with Dockerfile (e.g., random, f1, no_host, or intelact)

# Build a docker image named cig2017_${DIR}
./build.sh ${DIR} 

# Run a docker image named cig2017_${DIR}
./run.sh ${DIR}
```

### Provided Images
> By default, the agents connect to **localhost** and have the GUI window disabled. To customize this behavior change **_vizdoom.cfg** file and rebuild the image.

* [host](host) - the image will be used for the initialization of the game. All agents are supposed to connect to the host. By default, the host creates a 10-minutes deathmatch for 1 player on map01 with no bots. To change this behaviour use run.sh's optional parameters:

```
# Sample usage (a 12-minutes deathmatch for 8 players on map 1):
./run.sh host -p 8 -t 12 -m 1

usage: Host script for ViZDoom Copmetition at CIG 2017. [-h] [-b BOTS_NUM]
                                                        [-p PLAYERS_NUM]
                                                        [-m MAP]
                                                        [-t TIMELIMIT] [-c]
                                                        [-w]

optional arguments:
  -h, --help            show this help message and exit
  -b BOTS_NUM, --bots BOTS_NUM
                        number of bots to add [0,15] (default: 0)
  -p PLAYERS_NUM, --players PLAYERS_NUM
                        number of players [1,16] (default: 1)
  -m MAP, --map MAP     map number [1,5] (default: 1)
  -t TIMELIMIT, --time TIMELIMIT
                        timelimit in minutes [1,999] (default: 10)
  -c, --console         enable console (default: False)
  -w, --watch           roam the map as a ghost spectator (default: False)
```

* [random](random) - a random agent which connects to the host and does not do anything smart. By changing the mode to ASYNC_SPECTATOR and enabling window visibility in **_vizdoom.cfg** you can replace the random.
* [no_host](no_host) - random agent which does **NOT** connect to the host - it hosts a game for itself and can add built-in bots. This image will not be used by us but may be useful for training the agents. It runs faster since it is synchronized (mode=PLAYER)
* [f1](f1) - the winner entry of the ViZDoom Competition 2016 Limitted Deathmatch by **Yuxin Wu** and **Yuandong Tian**,
* [intelact](intelact) - the winner entry of the ViZDoom Competition 2016 Full Deathmatch (track 2) by **Alexey Dosovitskiy** and **Vladlen Koltun**.

### External files
Some entries were too big to be shared on github, so we provide them externally:
* [clyde](http://www.cs.put.poznan.pl/mkempka/misc/vdaic2016_agents/clyde.zip) - the 3rd place of the ViZDoom Competition 2016 Limitted Deathmatch by **Dino Ratcliffe**

* [2017 submissions](http://www.cs.put.poznan.pl/mkempka/misc/vdaic2017_agents/) - best submissions of Visual Doom AI Competitions **2017** (both tracks)

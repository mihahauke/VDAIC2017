# Sample submissions for [Visual Doom AI Competition 2017 at CIG2017](http://vizdoom.cs.put.edu.pl/competition-cig-2017)
>> Submissions require [Docker](https://www.docker.com/). All images except for the host require quite recent Nvidia drivers.
## How it will be run
We have prepared two wrapper scripts which will [build](build.sh) and [run](run.sh) docker images with agents and the [host](host)

To build and launch chosen container run:
```
DIR=host # or any other directory with Dockerfile

# Builds a docker image named cig2017_${DIR}
./build.sh ${DIR} 

# Runs docker image named cig2017_${DIR}
./run.sh ${DIR}
```

### Provided images:
> By default all agents connect to **localhost** and disable window. To customize this behavior change **_vizdoom.cfg** file.

* [host](host) - the image will be used for initiation the game. All agents are supposed to connect to the host. By default the host creates a deathmatch for 1 player on map01 with no bots lasting for 10 minutes but it's possible to override it with optional parameters.

```
# Sample usage (game for 8 players lasting 12 minutes on map 1):
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


* [random](random)- random agent which connects to the host and doesn't do anything smart. By changing mode to ASYNC_SPECTATOR and enabling window visibility in **_vizdoom.cfg** you can replace the random.
* [no_host](no_host) - random agent which does **NOT** connect to the host - it hosts a game for itself and can add bots. This image won't be used by us but may be useful for training on bots.
* [f1](f1) - winner submission of 2016 edition, track 1 by **Yuxin Wuand** and **Yuandong Tian**,
* [intelact](intelact) - winner submission of 2016 edition, track 2  by **Alexey Dosovitskiy** and **Vladlen Koltun**.


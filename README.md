# Docker-VapourSynth-Linux

## Software Versions

- python3: 3.9
- dgdemux: v1.0.0.50
- mediainfo: v21.03
- rclone: v1.55.0
- x264: x264-r3048-b86ae3c
- mkvtoolnix: 58.0.0

## Vapoursynth Plugins
* [vapoursynth-fillborders](https://github.com/dubhater/vapoursynth-fillborders)
* [Adaptivegrain-rs v0.3.1](https://git.kageru.moe/kageru/adaptivegrain)
* [RemapFrames v1.1](https://github.com/Irrational-Encoding-Wizardry/Vapoursynth-RemapFrames)

## Vapoursynth Python Module
* [awsmfunc](https://git.concertos.live/AHD/awsmfunc)
* [vardefunc](https://github.com/Ichunjo/vardefunc/)
## How to build the environment

```
docker-compose up -d
```

## How to enter the container

```
docker exec -it encode /bin/bash
```


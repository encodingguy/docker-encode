FROM encodeguy/vapoursynth-linux:v0
RUN pip install git+https://git.concertos.live/AHD/awsmfunc.git\
    && pip install git+https://github.com/Ichunjo/vardefunc.git
COPY vsplugin /usr/lib/x86_64-linux-gnu/vapoursynth/
COPY bin /usr/bin/
COPY ./ /root/dockerfile

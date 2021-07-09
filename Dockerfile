FROM encodeguy/vapoursynth-linux:v0
RUN pip3 install git+https://git.concertos.live/AHD/awsmfunc.git\
    && pip3 install git+https://github.com/Ichunjo/vardefunc.git\
    && pip3 install numpy
COPY vsplugin /usr/lib/x86_64-linux-gnu/vapoursynth/
COPY bin /usr/bin/
COPY ./ /root/dockerfile

FROM encodeguy/vapoursynth-yuuno:v0
RUN apt install -y unzip\
    && pip3 install git+https://git.concertos.live/AHD/awsmfunc.git\
    && pip3 install git+https://github.com/Ichunjo/vardefunc.git\
    && curl https://rclone.org/install.sh | bash
COPY vsplugin /usr/local/lib/vapoursynth/
COPY bin /usr/bin/
COPY ./ /root/dockerfile

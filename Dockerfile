FROM debian:bullseye
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update\
    && apt-get install -y wget curl\
    && echo "deb http://www.deb-multimedia.org bullseye main non-free" >> /etc/apt/sources.list\
    && wget http://www.deb-multimedia.org/pool/main/d/deb-multimedia-keyring/deb-multimedia-keyring_2016.8.1_all.deb\
    && dpkg -i deb-multimedia-keyring_2016.8.1_all.deb\
    && wget https://mediaarea.net/repo/deb/repo-mediaarea_1.0-16_all.deb\
    && dpkg -i repo-mediaarea_1.0-16_all.deb\
    && apt-get update\
    && apt-get update -oAcquire::AllowInsecureRepositories=true\
    && apt-get install -y deb-multimedia-keyring\
    && apt-get update\
    && apt-get install -y python python3 python3-pip git unzip vim mkvtoolnix\
    && apt-get install -y vapoursynth\
    && apt-get install -y mediainfo\
    && pip3 install jupyter\
    && rm -rf deb-multimedia-keyring_2016.8.1_all.deb\
    && rm -rf repo-mediaarea_1.0-16_all.deb\
    && apt-get clean\
    && apt-get autoremove \
    && pip3 install git+https://git.concertos.live/AHD/awsmfunc.git\
    && pip3 install git+https://github.com/Ichunjo/vardefunc.git\
    && pip3 install numpy
COPY vsplugin /usr/lib/x86_64-linux-gnu/vapoursynth/
COPY bin /usr/bin/
COPY ./ /root/dockerfile
ENV PYTHONPATH "${PYTHONPATH}:/python_module"

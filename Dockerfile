FROM yyfyyf/vapoursynth-yuuno:v1.0
RUN apt install -y unzip
    && curl https://rclone.org/install.sh | bash\
    &&
COPY vsplugin /usr/local/lib/vapoursynth/
COPY bin /usr/bin/

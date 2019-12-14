FROM ubuntu:bionic

WORKDIR /musicxml2video

RUN apt-get update && \
    apt-get install -y ffmpeg python python-pip && \
    pip install pydub ffmpeg-python

ENTRYPOINT [ "python", "main.py" ]

RUN pwd

COPY main.py config.py audio_process.py  musicxml_processor.py video_process.py ./
COPY input input
COPY utils utils

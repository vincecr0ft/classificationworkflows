FROM rootproject/root-ubuntu16

USER root

RUN mkdir /code
COPY . /code

WORKDIR /code
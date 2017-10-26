FROM ubuntu:16.04

MAINTAINER Naveena Ajjugottu <ajjugottu.naveena@gmail.com>

WORKDIR /usr/local/bin

RUN set -ex \
  && apt-get update -y \
  && apt-get install -y vim git python3 unzip \
  && git clone https://github.com/vangalamaheshh/nLogReporter.git


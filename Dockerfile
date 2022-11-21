# BASE: https://github.com/ryankurte/docker-ns3
FROM ubuntu:latest
MAINTAINER VANETLAB INCORPORATED 
LABEL Description="dockerized VANETlab backend for FE development on windows OS"

RUN apt-get update

# General dependencies
RUN apt-get install -y \
  git \
  mercurial \
  wget \
  vim \
  autoconf \
  bzr \
  cvs \
  unrar \
  build-essential \
  clang \
  valgrind \
  gsl-bin \
  libgslcblas0 \
  libgsl-dev \
  flex \
  bison \
  libfl-dev \
  tcpdump \
  sqlite \
  sqlite3 \
  libsqlite3-dev \
  libxml2 \
  libxml2-dev \
  vtun \
  lxc

# QT4 components
RUN apt-get install -y \
  qtbase5-dev

# Python components
RUN apt-get install -y \
  python3 \
  python3-dev \
  python3-setuptools \
  cmake \
  libc6-dev \
  libc6-dev-i386 \
  g++-multilib

# Dependencies for outdated python versions
RUN apt-get install -y \
  software-properties-common 

# Add repository for outdated python versions
RUN add-apt-repository ppa:deadsnakes/ppa 

# Update repository
RUN apt update -y

# Install TZ-data
RUN DEBIAN_FRONTEND=noninteractive TZ=Etc/UTC apt-get -y install tzdata

# Get python3.8 because we need python<3.9
RUN apt-get install -y \
  python3.8 \
  python3.8-distutils \
  python3.8-dev 

# Get pip
RUN cd /tmp && wget https://bootstrap.pypa.io/get-pip.py && \
  python3.8 /tmp/get-pip.py 

# install pybindgen
RUN python3.8 -m pip install pybindgen

# NS-3

# Create working directory
RUN mkdir -p /usr/ns3
WORKDIR /usr

# Clone NS-3 Allinone
RUN git clone https://gitlab.com/nsnam/ns-3-allinone.git

# Download NS-3.30
RUN cd ns-3-allinone && ./download.py -n ns-3.30

# Build and NS-3
RUN cd ns-3-allinone && ./build.py --enable-examples --enable-tests || true

# configure NS-3
RUN cd ns-3-allinone/ns-3.30 && ./waf configure || true && python3.8 ./waf configure || true

# Clone VANETlab Backend
RUN git clone https://github.com/vanetnuggets/vanetlab-be 

# Install VANETlab Backend
RUN cd vanetlab-be && python3.8 -m pip install -r requirements.txt 

# Set environment variable for ns3 WAF
ENV NS3_WAF_PATH="/usr/ns-3-allinone/ns-3.30"

# Open PORT
EXPOSE 9000/tcp

# Start API
RUN cd vanetlab-be && python3.8 main.py
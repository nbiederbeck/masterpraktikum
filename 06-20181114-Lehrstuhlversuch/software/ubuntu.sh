#!/bin/bash
sudo apt-get update
sudo apt-get install -y \
    git dpkg-dev make g++ gcc binutils \
    libx11-dev libxpm-dev libxft-dev libxext-dev htop \
    build-essential curl gfortran libssl-dev libpcre3-dev \
    xlibmesa-glu-dev libglew1.5-dev libftgl-dev \
    libmysqlclient-dev libfftw3-dev libcfitsio-dev \
    graphviz-dev libavahi-compat-libdnssd-dev \
    libldap2-dev python-dev libxml2-dev libkrb5-dev \
    libgsl0-dev libqt4-dev cmake libnova-dev vim

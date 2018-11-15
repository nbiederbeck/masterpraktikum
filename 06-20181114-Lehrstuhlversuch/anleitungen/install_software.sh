#!/bin/bash

# Installation der Software
# *getestet auf Ubuntu 18.04*

# Zuerst müssen die notwendigen Abhängigkeiten installiert werden.
sudo apt-get update
sudo apt-get install -y \
    git dpkg-dev make g++ gcc binutils \
    libx11-dev libxpm-dev libxft-dev libxext-dev htop \
    build-essential curl gfortran libssl-dev libpcre3-dev \
    xlibmesa-glu-dev libglew1.5-dev libftgl-dev \
    libmysqlclient-dev libfftw3-dev libcfitsio-dev \
    graphviz-dev libavahi-compat-libdnssd-dev \
    libldap2-dev python-dev libxml2-dev libkrb5-dev \
    libgsl0-dev libqt4-dev cmake subversion libnova-dev vim

# Dann wird Anaconda installiert.
curl -O -L https://repo.continuum.io/archive/Anaconda3-5.3.0-Linux-x86_64.sh
bash Anaconda3-5.3.0-Linux-x86_64.sh -p $HOME/.local/anaconda3 -b
$HOME/.local/anaconda3/bin/conda install libgcc=5 --yes
rm Anaconda3-5.3.0-Linux-x86_64.sh

# Jetzt muss eine gepatchte root5 Version heruntergeladen werden.
cd $HOME/.local
curl -L  https://github.com/root-project/root/archive/v5-34-00-patches.tar.gz | tar xzv

# Zum Bauen von root muss das System-Python verwendet werden!
# Also wird der `$PATH` kurzzeitig angepasst.
export PATH="/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin"

# Danach kann root konfiguriert werden.
mkdir root-5-34-anaconda3
cd root-5-34-anaconda3
cmake \
    -D builtin_zlib=ON \
    -D mathmore=ON \
    -D minuit2=ON \
    ../root-5-34-00-patches
cmake \
    -D builtin_zlib=ON \
    -D mathmore=ON \
    -D minuit2=ON \
    -D PYTHON_EXECUTABLE=$HOME/.local/anaconda3/bin/python \
    -D PYTHON_INCLUDE_DIR=$HOME/.local/anaconda3/include/python3.6m \
    -D PYTHON_LIBRARY=$HOME/.local/anaconda3/lib/libpython3.6m.so \
    ../root-5-34-00-patches
# Und anschließend gebaut werden (dieser Schritt wird am längsten dauern).
cmake --build .
source bin/thisroot.sh

# Ladet danach die Mars Software herunter.
cd ..
curl -OL https://magicdata.app.tu-dortmund.de/lehrstuhlversuch/Mars_V2-19-2.tgz \
    -u username:password
# Den `username` und das `password` erhaltet ihr von der Assistentin.

# Dekomprimieren und Entpacken.
gunzip Mars_V2-19-2.tgz; tar xf Mars_V2-19-2.tar
rm Mars_V2-19-2.tar
cd Mars_V2-19-2

# Mars bauen.
make mproper
make

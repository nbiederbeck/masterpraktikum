#!/bin/bash

# Installation der Software
# *getestet auf Ubuntu 18.04*

# Zuerst müssen die notwendigen Abhängigkeiten installiert werden.
bash $1.sh

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
    -Wno-dev \
    ../root-5-34-00-patches
cmake \
    -D builtin_zlib=ON \
    -D mathmore=ON \
    -D minuit2=ON \
    -D PYTHON_EXECUTABLE=$HOME/.local/anaconda3/bin/python \
    -D PYTHON_INCLUDE_DIR=$HOME/.local/anaconda3/include/python3.7m \
    -D PYTHON_LIBRARY=$HOME/.local/anaconda3/lib/libpython3.7m.so \
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

# Variablen exportieren
export MARSSYS=$(pwd)
export LD_LIBRARY_PATH=$ROOTSYS/lib:$MARSSYS:$LD_LIBRARY_PATH
export DYLD_LIBRARY_PATH=$LD_LIBRARY_PATH
export PATH=$ROOTSYS/bin:$MARSSYS:$PATH
export OSTYPE=$OSTYPE

# Mars bauen.
make mrproper
make

# Um die Software im Anschluss und nach Neustarts etc. nutzen zu können,
# müssen folgende Zeilen in der `~/.bashrc` eingetragen werden.
echo "
# MAGIC SOftware
export PATH=$PATH:$HOME/.local/anaconda3/bin
export ROOTSYS=$HOME/.local/root-5-34-anaconda3
export MARSSYS=$HOME/.local/Mars_V2-19-2
export LD_LIBRARY_PATH=$ROOTSYS/lib:$MARSSYS:$LD_LIBRARY_PATH
export DYLD_LIBRARY_PATH=$LD_LIBRARY_PATH
export PATH=$ROOTSYS/bin:$MARSSYS:$PATH
" >> ~/.bashrc

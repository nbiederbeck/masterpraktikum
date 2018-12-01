#!/bin/bash
sudo pacman -Syu \
    git make gcc binutils \
    libx11 libxpm libxft libxext htop \
    curl gcc-libs openssl pcre2 \
    mesa glu glew ftgl \
    mariadb-clients fftw cfitsio \
    graphviz avahi \
    libldap python libxml2 expat krb5 \
    gsl cmake libnova vim

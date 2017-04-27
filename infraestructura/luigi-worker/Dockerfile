FROM python:3.5-slim

MAINTAINER Denisse Martínez "denisse.martinez.m@gmail.com"

ENV LUIGI_HOME /etc/luigi

RUN apt-get update -yq

RUN apt-get install -yqq ssh git build-essential

ADD requirements.txt /tmp/requirements.txt
RUN pip install -r /tmp/requirements.txt

RUN mkdir $LUIGI_HOME

#Variables para el usuario
ARG FDC_USER
ARG FDC_UID

ARG GITHUB_REPO
ARG GITHUB_USER

ARG OUTPUT_DIR

ENV GITHUB_REPO fuga-de-cerebros
ENV GITHUB_USER ITAM-DS

#Creamos al usuario que ejecuta el worker
RUN useradd -m -s /bin/bash -N -u $FDC_UID $FDC_USER

RUN mkdir /home/$FDC_USER/.ssh

#Agregamos llave de github
ADD id_rsa /home/$FDC_USER/.ssh

RUN chmod 600 /home/$FDC_USER/.ssh/id_rsa

RUN touch /home/$FDC_USER/.ssh/known_hosts

RUN ssh-keyscan -T 60 github.com >> /home/$FDC_USER/.ssh/known_hosts

#Ajustamos permisos
RUN chown -R  $FDC_USER:users -R /home/$FDC_USER

USER $FDC_USER

WORKDIR /home/$FDC_USER

RUN git clone git@github.com:$GITHUB_USER/$GITHUB_REPO.git 

WORKDIR /home/$FDC_USER/$GITHUB_REPO/etl

ADD Makefile .

CMD [ "/bin/sh", "-c", "while true; do echo hello world; sleep 1; done"]

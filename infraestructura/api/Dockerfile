FROM python:3.5-slim

MAINTAINER "sharop@gmail.com"

RUN apt-get update -yq

RUN apt-get install -yqq build-essential ssh git

ADD requirements.txt /tmp/requirements.txt
RUN pip install -r /tmp/requirements.txt

##Variable del usuario
ARG FDC_USER
ARG FDC_UID

ARG GITHUB_REPO
ARG GITHUB_USER
ARG OUTPUT_DIR

RUN useradd -m -s /bin/bash -N -u $FDC_UID $FDC_USER

RUN mkdir /home/$FDC_USER/.ssh

#AGREGAMOS AL USUARIO QUE EJECUTA EL DOCKER
ADD id_rsa /home/$FDC_USER/.ssh

RUN chmod 600 /home/$FDC_USER/.ssh/id_rsa

RUN touch /home/$FDC_USER/.ssh/known_hosts

RUN ssh-keyscan -T 60 github.com >> /home/$FDC_USER/.ssh/known_hosts

### ajustamos permisos de la llave
RUN chown -R $FDC_USER:users -R /home/$FDC_USER

USER $FDC_USER

WORKDIR /home/$FDC_USER

RUN git clone git@github.com:$GITHUB_USER/$GITHUB_REPO.git

WORKDIR /home/$FDC_USER/$GITHUB_REPO/src/rest_api

EXPOSE 5000

CMD [ "python",  "./app.py"]

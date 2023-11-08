FROM ubuntu:latest

ENV PYTHON_VERSION 3.11
ENV HOME /root
ENV PYTHON_ROOT $HOME/local/python-$PYTHON_VERSION
ENV PATH $PYTHON_ROOT/bin:$PATH
ENV PYENV_ROOT $HOME/.pyenv

# タイムゾーン
RUN ln -sf /usr/share/zoneinfo/Asia/Tokyo /etc/localtime

# apt
RUN apt update
RUN apt install -y libopencv-dev

# install python and nodejs
RUN apt install -y python3.11-venv python3-pip nodejs npm curl

# update nodejs and npm
RUN npm install n -g
RUN n stable
RUN apt purge -y nodejs npm && apt autoremove -y

# install firebase
RUN npm install -g firebase-tools
FROM ubuntu:bionic

ENV PYTHONUNBUFFERED 1
ENV DEBIAN_FRONTEND noninteractive
ENV LANG C.UTF-8

RUN mkdir -p /app/screenshots

RUN apt-get -qq update && apt-get install -qq -y \
    build-essential \
    nodejs npm\
    git wget less nano curl \
    ca-certificates \
    gettext \
    python3.7-dev python3.7-distutils && \
    apt-get clean all && rm -rf /var/apt/lists/* && rm -rf /var/cache/apt/*

# install pip
RUN wget https://bootstrap.pypa.io/get-pip.py && python3.7 get-pip.py && rm get-pip.py
RUN pip3 install --no-cache-dir setuptools wheel -U

RUN useradd -ms /bin/bash django

COPY src /app/src

RUN chown django:django -R /app

COPY requirements.txt /app/requirements.txt
COPY package-lock.json /app/package-lock.json
RUN pip3 install --no-cache-dir -r /app/requirements.txt

USER django

EXPOSE 8000

WORKDIR /app/src
RUN npm install -g npm
RUN npm ci

VOLUME /app/screenshots

CMD ["gunicorn", "project.wsgi:application", "--bind", "0.0.0.0:8000"]

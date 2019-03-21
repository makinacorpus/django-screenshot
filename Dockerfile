FROM ubuntu:bionic

ENV PYTHONUNBUFFERED 1
ENV DEBIAN_FRONTEND noninteractive
ENV LANG C.UTF-8

RUN useradd -ms /bin/bash django
RUN mkdir -p /app

RUN apt-get -qq update && apt-get install -qq -y \
    build-essential \
    nodejs npm\
    chromium-browser \
    git wget less nano curl \
    ca-certificates \
    gettext \
    python3.7-dev python3.7-distutils && \
    apt-get clean all && rm -rf /var/apt/lists/* && rm -rf /var/cache/apt/*

RUN npm install -g npm

# install pip
RUN wget https://bootstrap.pypa.io/get-pip.py && python3.7 get-pip.py && rm get-pip.py

COPY requirements.txt /app/requirements.txt
COPY package.json /app/package.json
COPY package-lock.json /app/package-lock.json

RUN pip3 install --no-cache-dir -r /app/requirements.txt

COPY src /app/src

RUN chown django:django -R /app

USER django

EXPOSE 8000

WORKDIR /app/src

RUN npm ci

CMD ["gunicorn", "project.wsgi:application", "--bind", "0.0.0.0:8000"]

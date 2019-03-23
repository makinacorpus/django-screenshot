FROM ubuntu:bionic

ENV PYTHONUNBUFFERED 1
ENV DEBIAN_FRONTEND noninteractive
ENV LANG C.UTF-8
# use ubuntu chromium to prevent puppeteer dependencies
ENV PUPPETEER_SKIP_CHROMIUM_DOWNLOAD true
ARG NODE_ENV=production
RUN useradd -ms /bin/bash django
RUN mkdir -p /app

RUN apt-get -qq update && apt-get install -qq -y \
    build-essential \
    libpq-dev \
    nodejs npm \
    # use ubuntu chromium to prevent puppeteer dependencies
    chromium-browser \
    git wget less nano curl \
    ca-certificates \
    gettext \
    python3.7-dev python3.7-distutils && \
    apt-get clean all && rm -rf /var/apt/lists/* && rm -rf /var/cache/apt/*

# install pip & requirements
RUN wget https://bootstrap.pypa.io/get-pip.py && python3.7 get-pip.py && rm get-pip.py

COPY requirements.txt /requirements.txt

RUN pip3 install --no-cache-dir gunicorn
RUN pip3 install --no-cache-dir -r /requirements.txt

# upgrade npm & requirements
COPY package.json /package.json
COPY package-lock.json /package-lock.json
RUN npm install -g npm
RUN npm ci

COPY src /app/src

RUN chown django:django -R /app

USER django

EXPOSE 8000

WORKDIR /app/src


CMD ["gunicorn", "project.wsgi:application", "--bind", "0.0.0.0:8000"]

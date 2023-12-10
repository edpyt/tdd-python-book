FROM jenkins/jenkins:lts-alpine
USER root
RUN apk add --no-cache python3
RUN python3 -m ensurepip
RUN python3 -m pip install --upgrade pip
RUN if [ ! -e /usr/bin/pip ]; then ln -s pip3 /usr/bin/pip ; fi
RUN if [[ ! -e /usr/bin/python ]]; then ln -sf /usr/bin/python3 /usr/bin/python; fi
RUN rm -r /root/.cache
RUN apk add pkgconf
RUN apk add build-base
RUN apk add python3-dev

RUN apk add ca-certificates
RUN apk add curl
RUN apk add firefox
RUN apk add xvfb
RUN curl -L https://github.com/mozilla/geckodriver/releases/download/v0.33.0/geckodriver-v0.33.0-linux64.tar.gz | tar xz -C /usr/local/bin

RUN apk add npm
FROM python:3.11-slim-buster

WORKDIR /tdd.pythonbook.com

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apt-get update \
  && apt-get -y install netcat gcc \
  && apt-get clean

COPY requirements.txt requirements.txt

RUN pip install -r requirements.txt

COPY . /tdd.pythonbook.com

COPY deploy/subdomain/gunicorn/command.sh /gunicorn.sh
RUN chmod +x /gunicorn.sh

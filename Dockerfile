FROM python:3.11-slim

WORKDIR /app

COPY ./requirements.txt /app/requirements.txt

COPY ./.env /app/.env

RUN apt-get update && apt-get install -y build-essential git && pip install -r requirements.txt && pip install git+https://github.com/w4sk/papnt.git@main

COPY ./config.ini /usr/local/lib/python3.11/site-packages/papnt/config.ini 
FROM python:3.10-slim-buster

WORKDIR /code
COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt
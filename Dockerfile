FROM python:latest

WORKDIR /source

COPY requirement.txt /source/
RUN pip install -r requirement.txt

COPY . /source/
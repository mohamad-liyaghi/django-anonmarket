FROM python:3.11-alpine

ENV PYTHONUNBUFFERED=1

WORKDIR /backend

RUN pip install --upgrade pip 

COPY requirements.txt /backend

RUN pip install -r requirements.txt

COPY . /backend

EXPOSE 8000
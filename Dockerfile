FROM python:3.13.13-slim

WORKDIR /app

ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

COPY . /app

RUN pip install --upgrade pip 
RUN pip install -r requirements.txt


FROM python:3.11-slim
LABEL maintainer="artemkazakov947@gmail.com"

ENV PYTHONUNBUFFERED 1

WORKDIR be.codelines/

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY . .

RUN adduser \
    --disabled-password \
    --no-create-home \
    codelines-user

USER codelines-user

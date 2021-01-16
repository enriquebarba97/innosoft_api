FROM python:3.8

ENV PYTHONUNBUFFERED 1

WORKDIR /app

RUN git clone -b dep-docker https://github.com/enriquebarba97/innosoft_api.git .
RUN pip install -r requirements.txt

WORKDIR /app/docker

# local settings.py
RUN ls
ADD docker-settings.py /app/innosoft_api/innosoft_api/local_settings.py

WORKDIR /app/innosoft_api/innosoft_api
RUN echo test
RUN ls
RUN echo test

WORKDIR /app/innosoft_api

RUN ./manage.py collectstatic
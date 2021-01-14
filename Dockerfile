FROM python:3.8

ENV PYTHONUNBUFFERED 1

COPY . /code/
WORKDIR /code/
RUN python -m pip install --upgrade pip
RUN pip install -r requirements.txt

EXPOSE 9000
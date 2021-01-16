FROM python:3.8

ENV PYTHONUNBUFFERED 1

WORKDIR /code/

RUN git clone https://github.com/enriquebarba97/innosoft_api.git .

# local settings.py
ADD /code/docker/docker-settings.py /code/innosoft_api/local_settings.py
RUN python -m pip install --upgrade pip
RUN pip install -r requirements.txt
#
RUN python /code/innosoft_api/manage.py setup
RUN python ./innosoft_api/manage.py runserver 0.0.0.0:9000
#

EXPOSE 9000
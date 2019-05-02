# base img
FROM python:3.7

MAINTAINER Haibo Yan

ADD . /usr/src/app

WORKDIR /usr/src/app

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8000

CMD exec gunicorn miye.wsgi:application --bind 0.0.0.0:8000 --workers 3
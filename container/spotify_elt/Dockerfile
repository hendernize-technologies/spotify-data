FROM python:3.10-slim-buster

WORKDIR /usr/src/app

ADD ./container /container

COPY requirements.txt /container
ENV variables.env /stonk-scraper
RUN pip install -r requirements.txt --upgrade pip

COPY . /container

ENTRYPOINT [ "python", "./entrypoint.py" ]
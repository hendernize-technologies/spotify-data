FROM python:3.7.6

EXPOSE 8080

ADD ./container /container
WORKDIR /container

COPY requirements.txt /container
ENV variables.env /stonk-scraper
RUN pip install -r requirements.txt --upgrade pip

COPY . /container

# CMD tbd
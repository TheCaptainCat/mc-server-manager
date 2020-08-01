FROM python:3.8-slim-buster
WORKDIR /game
COPY server_rnr server_rnr
COPY requirements.txt requirements.txt
COPY game.py game.py

RUN mkdir /usr/share/man/man1/
RUN apt-get update -y && apt-get install -y openjdk-11-jre

RUN pip install -U pip
RUN pip install -r requirements.txt

CMD ["python", "game.py"]

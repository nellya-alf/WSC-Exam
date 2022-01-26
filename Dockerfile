FROM ubuntu:20.04

WORKDIR /Autoscaler

RUN apt-get update\
    && apt-get install azure-cli -y sudo

RUN apt install python3.8-venv -y sudo

RUN python3 -m venv /opt/venv

COPY requirements.txt .
RUN . /opt/venv/bin/activate && pip install -r requirements.txt

COPY . .

CMD . /opt/venv/bin/activate && exec python main.py
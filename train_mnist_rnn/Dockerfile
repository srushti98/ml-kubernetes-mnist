FROM ubuntu:18.04

RUN apt-get -s autoclean
RUN apt-get update

RUN  apt-get install -y \
    python3.6 python3-dev gcc \
    ca-certificates curl

RUN curl -fsSL https://bootstrap.pypa.io/pip/3.6/get-pip.py | python3.6

WORKDIR /app
ADD requirements.txt /app
RUN pip3 install --upgrade pip setuptools
RUN pip3 --no-cache-dir install -r requirements.txt

ADD main.py  /app/main.py

CMD [ "python3", "main.py"]


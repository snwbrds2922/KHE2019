FROM ubuntu:18.04

MAINTAINER snwbrds2922 <snwbrds2922@gmail.com>

RUN apt-get update && apt-get install -y python3 python3-pip
RUN pip3 install websockets
RUN pip3 install asyncio
RUN apt-get clean && rm -rf /var/lib/apt/lists/*

COPY server.py /

EXPOSE 8766

ENTRYPOINT python3 /server.py


FROM debian:bookworm-slim

ENV LC_ALL=C.UTF-8
ENV LANG=C.UTF-8

WORKDIR /opt/mumble-rest

ENV DEBIAN_FRONTEND noninteractive

RUN apt-get update && apt-get install -y \
    build-essential \
    libssl-dev \
    python3 \
    python3-pip \
    python3-venv \
    libevent-dev \
    software-properties-common

RUN apt-key adv --keyserver keyserver.ubuntu.com --recv B6391CB2CFBA643D && \
    apt-add-repository "deb http://zeroc.com/download/ice/3.7/debian12 stable main" && \
    apt-get update && apt-get install -y python3-zeroc-ice zeroc-ice-compilers

ADD requirements.txt /opt/mumble-rest/requirements.txt
RUN python3 -m venv --system-site-packages venv && \
    ./venv/bin/pip3 install -r requirements.txt


RUN apt-get autoremove -y build-essential && \
    rm -rf /var/lib/apt/lists/*


ADD . /opt/mumble-rest

CMD ["/opt/mumble-rest/venv/bin/uvicorn", "main:mumble_rest", "--host", "0.0.0.0", "--port", "2332"]
FROM dyne/devuan:ascii
ENV debian stretch

LABEL maintainer="DECODE team <decode@dyne.org>" \
homepage="https://github.com/decodeproject"


ENV LC_ALL C
ENV DEBIAN_FRONTEND noninteractive
ENV DYNESDK=https://sdk.dyne.org:4443/job

RUN apt-get -y update && apt-get -y upgrade

RUN git clone https://github.com/hyperledger/sawtooth-core /opt/sawtooth
RUN mkdir -p /var/log/sawtooth \
 && mkdir -p /etc/sawtooth/keys \
 && mkdir -p /var/lib/sawtooth

RUN git clone https://github.com/hyperledger/sawtooth-sdk-python.git /opt/sawtooth/sdk/python


RUN apt-get install -y -q python3-pip python3-zmq python3-yaml python3-setuptools \
					   	  python3-toml python3-colorlog python3-cbor python3-dev
RUN pip3 install grpcio-tools requests zenroom

COPY zenroom_sawtooth /opt/sawtooth/sdk/examples/zenroom_sawtooth

ENV PATH=$PATH:/opt/sawtooth/sdk/examples/zenroom_sawtooth

WORKDIR /opt/sawtooth


RUN echo "\033[0;32m--- Building zenroom-tp-python ---\n\033[0m" \
 && bin/protogen \
 && cd cli \
 && pip3 install -e . \
 &&	cd ../sdk/python \
 && pip3 install -e . \
 && cd ../examples/zenroom_sawtooth \
 && pip3 install -e .

CMD zenroom-tp-python -v -C tcp://localhost:4004


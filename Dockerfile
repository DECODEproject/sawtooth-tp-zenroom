FROM dyne/devuan:ascii
ENV debian stretch

LABEL maintainer="DECODE team <decode@dyne.org>" \
homepage="https://github.com/decodeproject"


ENV LC_ALL C
ENV DEBIAN_FRONTEND noninteractive
ENV DYNESDK=https://sdk.dyne.org:4443/job

RUN apt-get -y update && apt-get -y upgrade

# RUN mkdir -p /usr/share/man/man1/ \
# 	&& apt-get -yy update && apt-get -yy upgrade \
# 	&& apt-get -yy install supervisor daemontools \
# 	   		   	   tmux curl net-tools python3

# ENV BUILD_DEPS="build-essential zlib1g-dev gcc make autoconf automake pkg-config uuid-dev"
# RUN apt-get -yq install $BUILD_DEPS

RUN apt-get install -y -q python3-pip
# RUN pip3 install --upgrade pip3
RUN pip3 install grpcio-tools
RUN pip3 install zenroom

RUN git clone https://github.com/hyperledger/sawtooth-core /opt/sawtooth
RUN mkdir -p /var/log/sawtooth


COPY zenroom_python /opt/sawtooth/sdk/examples/zenroom_python


ENV PATH=$PATH:/opt/sawtooth/sdk/examples/zenroom_python

WORKDIR /opt/sawtooth

CMD echo "\033[0;32m--- Building zenroom-tp-python ---\n\033[0m" \
 && bin/protogen \
 && cd sdk/examples/zenroom_python \
 && python3 setup.py clean --all \
 && python3 setup.py build

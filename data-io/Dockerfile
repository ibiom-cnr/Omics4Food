FROM ubuntu:16.04

MAINTAINER Marco Tangaro <ma.tangaro@gmail.com>

COPY . /app
WORKDIR /app/

RUN apt-get update

RUN DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends curl python python-keystoneclient python-swiftclient python-pycurl python-jinja2

RUN rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

# Copy download script
COPY ./swift_download.py /usr/local/bin/swift-download
RUN chmod +x /usr/local/bin/swift-download

# Copy upload script
COPY ./swift_upload.sh /usr/local/bin/swift-upload
RUN chmod +x /usr/local/bin/swift-upload

# Copi lims API call script
COPY ./lims_api_call.sh /usr/local/bin/lims-api-call
RUN chmod +x /usr/local/bin/lims-api-call

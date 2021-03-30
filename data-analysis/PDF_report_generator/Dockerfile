FROM qiime2/core:2019.10

MAINTAINER Marco Tangaro <ma.tangaro@gmail.com>

COPY . /app
WORKDIR /app/


RUN pip install pdfkit

RUN apt-get update

RUN DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends wkhtmltopdf

RUN rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

RUN conda install -n qiime2-2019.10 biopython

RUN conda install -n qiime2-2019.10 argcomplete

RUN conda install -n qiime2-2019.10 -c conda-forge plotnine

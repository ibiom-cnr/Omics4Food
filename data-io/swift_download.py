#!/usr/bin/env python
"""
Contributors:
author: Tangaro Marco
email: ma.tangaro@ibiom.cnr.it
"""

import os, sys
import argparse
import urllib2
import logging
import pycurl
import tarfile
import datetime

#______________________________________
def parse_cli_options():
  parser = argparse.ArgumentParser(description='Download Galaxy tool dependency from Swift repository', formatter_class=argparse.RawTextHelpFormatter)
  parser.add_argument( '-u', '--url',  dest='data_url', default=None , help='Swift data URL')
  parser.add_argument( '-o', '--outdir', dest='outdir', default=None, help='Working directory')
  parser.add_argument( '-n', '--name', dest='data_input_name', default='data_input.tar.gz', help='Data input tar.gz name')
  return parser.parse_args()

#______________________________________
def create_dir(dirpath = 'directory_path'):
  if not os.path.exists(dirpath):
    os.makedirs(dirpath)

#______________________________________
def write_data(name, url):
  print(str(datetime.datetime.now()) + " - Downloading: " + str(url))
  try: 
    response = urllib2.urlopen(url)
    with open(name, "wb") as fp:
      curl = pycurl.Curl()
      curl.setopt(pycurl.URL, url)
      curl.setopt(pycurl.WRITEDATA, fp)
      curl.perform()
      curl.close()
      fp.close()
  except (urllib2.HTTPError):
    sys.stderr.write(str(datetime.datetime.now()) + " - File not found. Please check the input url.")
    sys.exit(1)

#______________________________________
# Extract tar.gz archive
def extract_tar_gz(tar_file):
  tar = tarfile.open(tar_file)
  tar.extractall()
  tar.close()

#______________________________________
def swift_download():
  options = parse_cli_options()

  print(str(datetime.datetime.now()) + " - >>> Start Swift data download")

  if options.data_url is None:
    raise Exception(str(datetime.datetime.now()) + " - No data url detected.")

  if options.outdir is None:
    raise Exception(str(datetime.datetime.now()) + " - No working directory detected.")

  create_dir(options.outdir)
  os.chdir(options.outdir)

  # download tar.gz
  logging.debug('Download tar.gz')
  write_data(options.data_input_name, options.data_url)

  # extract tar.gz
  logging.debug('Extract %s', options.data_input_name)
  extract_tar_gz(options.data_input_name)

  # remove tar.gz
  print(str(datetime.datetime.now()) + " - Removing tar.gz!")
  os.remove(options.data_input_name)
  print(str(datetime.datetime.now()) + " - File Removed!")

  # end
  print(str(datetime.datetime.now()) + " - Download END.")

#______________________________________
if __name__ == "__main__":
  swift_download()

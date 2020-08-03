#!/usr/bin/env python
"""
Contributors:
author: Tangaro Marco
email: ma.tangaro@ibiom.cnr.it
"""

import hashlib
import argparse

#______________________________________
def parse_cli_options():
  parser = argparse.ArgumentParser(description='Download Galaxy tool dependency from Swift repository', formatter_class=argparse.RawTextHelpFormatter)
  parser.add_argument( '-n', '--name',  dest='name', default=None , help='Name to Hash')
  return parser.parse_args()

#______________________________________
def createContainerId(name):
  hash = (name + '012345678012345678012345678012')[0:30]
  return hashlib.md5(hash.encode('utf-8')).hexdigest().upper()

#______________________________________
def create_container_id():

  options = parse_cli_options()

  print(createContainerId(options.name))

#______________________________________
if __name__ == "__main__":
  create_container_id()

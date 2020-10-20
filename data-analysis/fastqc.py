#!/usr/bin/env python

import os
import uuid
from jinja2 import Environment, FileSystemLoader
import requests
import json

template_dir = './templates'
endpoint = 'https://90.147.75.16:4443/v1/scheduler/iso8601'
endpoint_dependency = 'https://90.147.75.16:4443/v1/scheduler/dependency'
chronos_username = 'admin'

from getpass import getpass
print 'Type chronos password: '
chronos_password =  str(getpass())

#______________________________________
def create_uuid():
  return uuid.uuid4()

#______________________________________
def post(url, json):

  headers = {'Content-Type': 'application/json'}

  response = requests.post(url, json=json, headers=headers, auth=(chronos_username, chronos_password), verify=False)

  return response

#______________________________________
def get_json(template_name, template_dir, uuid):

  env = Environment( loader=FileSystemLoader(template_dir) )

  template = env.get_template(template_name)

  rendered_template = template.render(job_run_id=uuid)

  print rendered_template

  payload = json.loads(rendered_template)

  return payload

#______________________________________
def run():

  lst = os.listdir(template_dir)
  lst.sort()
  print lst

  ### Data download

  # generate parent uuid
  uuid = create_uuid()

  # Download data
  data_download = get_json("./fastqc/data_download.json", template_dir, uuid)
  post(endpoint, data_download)

  # Run fastqc
  run_fastqc = get_json("./fastqc/fastqc.json", template_dir, uuid)
  post(endpoint_dependency, run_fastqc)

  # Create output tar file
  prepare_output = get_json("./fastqc/prepare_data_upload.json", template_dir, uuid)
  post(endpoint_dependency, prepare_output)

  # Upload file to Swift
  data_upload = get_json("./fastqc/data_upload.json", template_dir, uuid)
  post(endpoint_dependency, data_upload)


#______________________________________
if __name__ == '__main__':
  run()

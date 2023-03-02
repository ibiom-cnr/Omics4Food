#!/usr/bin/env python

import os
import uuid
from jinja2 import Environment, FileSystemLoader
import requests
import json
import argparse

template_dir = './templates'
endpoint = 'https://90.147.75.16:4443/v1/scheduler/iso8601'
endpoint_dependency = 'https://90.147.75.16:4443/v1/scheduler/dependency'
chronos_username = 'admin'

from getpass import getpass
print 'Type chronos password: '
chronos_password =  getpass()


def cli_options():
  parser = argparse.ArgumentParser(description='GeneView Render script')
  parser.add_argument('--uuid', dest='user_uuid', help='Specific UUID from previous workflow step')

  return parser.parse_args()

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

  options = cli_options()

  lst = os.listdir(template_dir)
  lst.sort()
  print lst

  ### Data download

  # generate parent uuid
  uuid=None
  print(options.user_uuid)
  if options.user_uuid is not None:
    uuid = options.user_uuid
  else:
    uuid = create_uuid()

  # Download data
  data_download = get_json("./qiime2_pe_diversity/data_download.json", template_dir, uuid)
  post(endpoint, data_download)

  # Create core-metrics-phylogenetic
  run_step_01 = get_json("./qiime2_pe_diversity/qiime2_diversity.1.json", template_dir, uuid)
  post(endpoint_dependency, run_step_01)

  # Feature classifier
  run_step_02 = get_json("./qiime2_pe_diversity/qiime2_diversity.2.json", template_dir, uuid)
  post(endpoint_dependency, run_step_02)

  # Metadata tabulate
  run_step_03 = get_json("./qiime2_pe_diversity/qiime2_diversity.3.json", template_dir, uuid)
  post(endpoint_dependency, run_step_03)

  # Barplot creation
  run_step_04 = get_json("./qiime2_pe_diversity/qiime2_diversity.4.json", template_dir, uuid)
  post(endpoint_dependency, run_step_04)

  # Create pdf report
  run_step_05 = get_json("./qiime2_pe_diversity/qiime2_diversity.5.json", template_dir, uuid)
  post(endpoint_dependency, run_step_05)

  # Create output tar file
  prepare_output = get_json("./qiime2_pe_diversity/prepare_data_upload.json", template_dir, uuid)
  post(endpoint_dependency, prepare_output)

  # Upload file to Swift
  data_upload = get_json("./qiime2_pe_diversity/data_upload.json", template_dir, uuid)
  post(endpoint_dependency, data_upload)


#______________________________________
if __name__ == '__main__':
  run()

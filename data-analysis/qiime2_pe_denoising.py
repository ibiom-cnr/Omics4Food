#!/usr/bin/env python

import os
import uuid
from jinja2 import Environment, FileSystemLoader
import requests
import json
import argparse
import sys

template_dir = './templates'
endpoint = 'https://90.147.75.16:4443/v1/scheduler/iso8601'
endpoint_dependency = 'https://90.147.75.16:4443/v1/scheduler/dependency'
chronos_username = 'admin'

from getpass import getpass
print 'Type chronos password: '
chronos_password =  getpass()


#______________________________________
def cli_options():
  parser = argparse.ArgumentParser(description='GeneView Render script')
  parser.add_argument('--demultiplexed', dest='demultiplexed_data', default=False, action='store_true', help='Analyse demultiplexed data')
  parser.add_argument('--multiplexed', dest='multiplexed_data', default=False, action='store_true', help='Analyse multiplexed data')
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

  if not options.demultiplexed_data and not options.multiplexed_data:
    print '[ERROR] Select multiplexed or demultiplexed data workflow'
    sys.exit(1)

  if options.demultiplexed_data and options.multiplexed_data:
    print '[ERROR] Select only one of multiplexed or demultiplexed data workflow'
    sys.exit(1) 

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
  data_download = get_json("./qiime2_pe_denoising/data_download.json", template_dir, uuid)
  post(endpoint, data_download)

  if options.demultiplexed_data and not options.multiplexed_data:

    ## Qiime Import
    run_step_01 = get_json("./qiime2_pe_denoising/qiime2_import_demultiplexed.json", template_dir, uuid)
    post(endpoint_dependency, run_step_01)

    ## WARNING!!!
    ## For DeMultiplexed data, step 2 is skipped.

  elif options.multiplexed_data and not options.demultiplexed_data:

    ## Qiime Import
    run_step_01 = get_json("./qiime2_pe_denoising/qiime2_denoising.1.json", template_dir, uuid)
    post(endpoint_dependency, run_step_01)

    ## Qiime Demux
    run_step_02 = get_json("./qiime2_pe_denoising/qiime2_denoising.2.json", template_dir, uuid)
    post(endpoint_dependency, run_step_02)

  run_step_03 = get_json("./qiime2_pe_denoising/qiime2_denoising.3.json", template_dir, uuid)
  post(endpoint_dependency, run_step_03)

  ## DADA2
  run_step_04 = get_json("./qiime2_pe_denoising/qiime2_denoising.4.json", template_dir, uuid)
  post(endpoint_dependency, run_step_04)

  ## FeatureTable and FeatureData summaries 
  run_step_05 = get_json("./qiime2_pe_denoising/qiime2_denoising.5.json", template_dir, uuid)
  post(endpoint_dependency, run_step_05)

  run_step_06 = get_json("./qiime2_pe_denoising/qiime2_denoising.6.json", template_dir, uuid)
  post(endpoint_dependency, run_step_06)

  ## Metadata tabulate
  run_step_07 = get_json("./qiime2_pe_denoising/qiime2_denoising.7.json", template_dir, uuid)
  post(endpoint_dependency, run_step_07)

  ## Generate a tree for phylogenetic diversity analyses
  run_step_08 = get_json("./qiime2_pe_denoising/qiime2_denoising.8.json", template_dir, uuid)
  post(endpoint_dependency, run_step_08)

  ## Export output
  run_step_09 = get_json("./qiime2_pe_denoising/qiime2_denoising.9.json", template_dir, uuid)
  post(endpoint_dependency, run_step_09)

  ## Biom Summarize table
  run_step_10 = get_json("./qiime2_pe_denoising/qiime2_denoising.10.json", template_dir, uuid)
  post(endpoint_dependency, run_step_10)

  ## Create output tar file
  prepare_output = get_json("./qiime2_pe_denoising/prepare_data_upload.json", template_dir, uuid)
  post(endpoint_dependency, prepare_output)

  ## Upload file to Swift
  data_upload = get_json("./qiime2_pe_denoising/data_upload.json", template_dir, uuid)
  post(endpoint_dependency, data_upload)


#______________________________________
if __name__ == '__main__':
  run()

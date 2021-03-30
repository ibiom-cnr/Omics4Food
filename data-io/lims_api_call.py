#!/usr/bin/env python

import sys
from jinja2 import Template, Environment, FileSystemLoader
import json
import argparse
import requests

#______________________________________
def cli_options():

  parser = argparse.ArgumentParser(description='Render jinja template and submit cURL')

  parser.add_argument('--lims-api-url', dest='lims_api_url', help='LIMS api url')
  parser.add_argument('--lims-nomeserver', dest='lims_nomeserver', help='LIMS nomeserver')
  parser.add_argument('--lims-idtenant', dest='lims_idtenant', help='LIMS IdTenant')
  parser.add_argument('--lims-username', dest='lims_username', help='LIMS username')
  parser.add_argument('--lims-password', dest='lims_password', help='LIMS user password')
  parser.add_argument('--id', dest='job_run_id', help='Job Run Unique ID')
  parser.add_argument('--url', dest='job_output_url', help='Job output URL')
  parser.add_argument('--dir', dest='template_dir', help='Template path')
  parser.add_argument('--template', dest='template', help='Template')

  return parser.parse_args()


#______________________________________
def lims_api_call():

  options = cli_options()

  env = Environment( loader=FileSystemLoader(options.template_dir) )

  template = env.get_template(options.template)

  rendered_template = template.render( lims_idtenant=options.lims_idtenant,
                                       lims_username=options.lims_username,
                                       lims_password=options.lims_password,
                                       job_run_id=options.job_run_id,
                                       job_output_url=options.job_output_url )

  print rendered_template

  headers={'Content-Type': 'application/json; charset=UTF-8', 'Host': options.lims_nomeserver }

  resp = requests.post( options.lims_api_url,
                        headers=headers,
                        data=rendered_template )

  print resp.status_code
  print resp.content

  if resp.status_code != '200':
    sys.exit(1)

#______________________________________
if __name__ == '__main__':
  lims_api_call()

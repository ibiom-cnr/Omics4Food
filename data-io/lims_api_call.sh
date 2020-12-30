#!/bin/bash

# This script explit a set of environment variable that has to be setup before using it.
# The following variables are mandatory!
#
# Environment variables example:
# export RECAS_URL_PREFIX="http://cloud.recas.ba.infn.it:8080/v1/AUTH_cf2db2690546474f889e300445b3bf20"
# export USERNAME="testservizi"
# export PROJECT_ID="3"
# export OUTPUT_FILENAMES="output_{{ job_run_id }}/fastqc.tar.gz" # example: export OUTPUT_FILENAMES="output_376e18e5-fe11-491f-8111-2d6828cfee6b/fastqc.tar.gz"
# export LIMS_API_METHOD="POST" # api_methods, e.g. GET, POST, ...
# export LIMS_API_URL="http://90.147.75.142:5000/lims_api_mock/v1.0/update-output-url"
#
# User input:
# $1: job_run_id
#
# Usage example:
# bash lims_api_call.sh 376e18e5-fe11-491f-8111-2d6828cfee6b
#

# Get Job Run Unique ID
JOB_RUN_ID=$1

# Build output url
username_hash=$(python ./create_container_id.py -n $USERNAME)
project_id_hash=$(python ./create_container_id.py -n $PROJECT_ID)
OUTPUT_PATH="$RECAS_URL_PREFIX/$username_hash/$project_id_hash/$OUTPUT_FILENAMES"

# Render json from jinja2 template
output_json=$(python render_output_json.py --id $JOB_RUN_ID --url $OUTPUT_PATH --dir . --template output.json.j2)
echo $output_json

# Call LIMS API
env
curl --header "Content-Type: application/json" --request $LIMS_API_METHOD --data "$output_json" $LIMS_API_URL

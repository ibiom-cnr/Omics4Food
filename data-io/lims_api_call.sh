#!/bin/bash

# Input:
# $1: job_run_id
# $2: username
# $3: project_id
# $4: output_filenames
# $5: api_methods, e.g. GET, POST, ...
# $6: lims_api_url, e.g. http://90.147.75.142:5000/lims_api_mock/v1.0/update-output-url
#
# Usage example:
# bash lims_api_call.sh 376e18e5-fe11-491f-8111-2d6828cfee6b testservizi 3 output_376e18e5-fe11-491f-8111-2d6828cfee6b/qiime2_se_diversity.tar.gz POST http://90.147.75.142:5000/lims_api_mock/v1.0/update-output-url
#

# Get Job Run Unique ID
JOB_RUN_ID=$1

# Build output url
output_url_prefix="http://cloud.recas.ba.infn.it:8080/v1/AUTH_cf2db2690546474f889e300445b3bf20"
username=$(python ./create_container_id.py -n $2)
project_id=$(python ./create_container_id.py -n $3)
output_filenames=$4
OUTPUT_PATH="$output_url_prefix/$username/$project_id/$output_filenames"

# Render json from jinja2 template
output_json=$(python render_output_json.py --id $JOB_RUN_ID --url $OUTPUT_PATH --dir . --template output.json.j2)
echo $output_json

# Call LIMS API
env
LIMS_API_METHOD=$5
LIMS_API_URL=$6
curl --header "Content-Type: application/json" --request $LIMS_API_METHOD --data "$output_json" $LIMS_API_URL

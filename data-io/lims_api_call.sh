#!/bin/bash

# This script explit a set of environment variable that has to be setup before using it.
# The following variables are mandatory!
#
# Environment variables example:
# Mesos variables
# export JOB_RUN_ID="{{ job_run_id }}" # example export JOB_RUN_ID="376e18e5-fe11-491f-8111-2d6828cfee6b"
# export OUTPUT_FILENAMES="output_{{ job_run_id }}/fastqc.tar.gz" # example: export OUTPUT_FILENAMES="output_376e18e5-fe11-491f-8111-2d6828cfee6b/fastqc.tar.gz"
#
# ReCaS variables
# export RECAS_URL_PREFIX="http://cloud.recas.ba.infn.it:8080/v1/AUTH_cf2db2690546474f889e300445b3bf20"
#
# LIMS variables
# export LIMS_IDTENANT="00000000-0000-0000-0000-000000000000" # Lims
# export LIMS_USERNAME="testservizi" # Lims
# export LIMS_PASSWORD="****" # Lims
# export LIMS_PROJECT_ID="3"
# export LIMS_NOMESERVER="****"
# export LIMS_API_METHOD="POST" # api_methods, e.g. GET, POST, ...
# export LIMS_API_URL="****"
#
# Usage example:
# bash lims_api_call.sh
#

# Build output url
username_hash=$(python ./create_container_id.py -n $LIMS_USERNAME)
project_id_hash=$(python ./create_container_id.py -n $LIMS_PROJECT_ID)
OUTPUT_PATH="$RECAS_URL_PREFIX/$username_hash/$project_id_hash/$OUTPUT_FILENAMES"

# Render json from jinja2 template
output_json=$(python render_output_json.py --lims-idtenant $LIMS_IDTENANT --lims-username $LIMS_USERNAME --lims-password $LIMS_PASSWORD --id $JOB_RUN_ID --url $OUTPUT_PATH --dir . --template output.json.j2)
echo $output_json

# Call LIMS API
env
curl --header "Conten-tType: application/json; charset=utf-8; Host: $LIMS_NOMESERVER" --http1.1 --request $LIMS_API_METHOD --data "$output_json" $LIMS_API_URL

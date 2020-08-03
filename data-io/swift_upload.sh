#!/bin/bash


username=$(python ./create_container_id.py -n $1)
project_id=$(python ./create_container_id.py -n $2)
export OUTPUT_PATH="$username/$project_id"

echo $OUTPUT_PATH

env
curl -s https://raw.githubusercontent.com/ibiom-cnr/Omics4Food/master/data-io/main.py | python || exit 1

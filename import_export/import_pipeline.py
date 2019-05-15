#!/usr/bin/env python

"""Demonstrates how to import a pipeline to Data Collector with Control Hub metadata"""

import sys
import json
import requests
from streamsets.sdk import DataCollector

# Static Vars
sdc_url = 'http://ec2-3-83-225-115.compute-1.amazonaws.com:18630'
sdc_user = 'admin'
sdc_pass = 'admin'

# Command line args
if len(sys.argv) != 3:
    print('Error: Wrong number of arguments')
    print('Usage: python import_pipeline.py <path_to_pipeline> <path_to_commit_metadata>')
    quit(1)

path_to_pipeline = sys.argv[1]
path_to_commit_metadata = sys.argv[2]


# Common headers for API calls
api_headers = {}
api_headers['Content-type'] = 'application/json; charset=utf-8'
api_headers['X-Requested-By'] = 'SDC'
api_headers['X-SS-REST-CALL'] = 'true'


# Import the pipeline
with open(path_to_pipeline, 'r', encoding='utf-8') as input_file:
    pipeline_json = json.load(input_file)

sdc = DataCollector(sdc_url, username=sdc_user, password=sdc_pass)
pipeline = sdc.import_pipeline(pipeline=pipeline_json)


# Update the pipeline metadata
with open(path_to_commit_metadata, 'r', encoding='utf-8') as input_file:
    metadata_json = json.load(input_file)

metadata_endpoint = sdc_url + '/rest/v1/pipeline/' + pipeline.id + '/metadata'

response = requests.post(url=metadata_endpoint, headers=api_headers, auth=(sdc_user, sdc_pass),
                         data=json.dumps(metadata_json))

if response.status_code != 200:
    print('Error updating pipeline metadata')
    print(response.status_code)
    print(response.text)
    quit(-1)

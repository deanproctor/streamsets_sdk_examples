#!/usr/bin/env python

"""Demonstrates how to import a pipeline to Control Hub, saving metadata for Data Collector"""

import sys
import json
import requests

# Static Vars
sch_url = 'http://ec2-3-81-36-29.compute-1.amazonaws.com:18631'
sch_creds = {"userName": "admin@admin", "password": "admin@admin"}


# Command line args
if len(sys.argv) != 4:
    print('Error: Wrong number of arguments')
    print('Usage: python commit_pipeline.py <path_to_pipeline> <commit_message> \
          <path_to_commit_metadata>')
    quit(1)

path_to_pipeline = sys.argv[1]
commit_message = sys.argv[2]
path_to_commit_metadata = sys.argv[3]


# Common headers for API calls
api_headers = {}
api_headers['Content-type'] = 'application/json; charset=utf-8'
api_headers['X-Requested-By'] = 'SDC'
api_headers['X-SS-REST-CALL'] = 'true'


# Get SCH Auth Token
auth_endpoint = sch_url + '/security/public-rest/v1/authentication/login'

auth_request = requests.post(url=auth_endpoint, headers=api_headers, data=json.dumps(sch_creds))

api_headers['X-SS-User-Auth-Token'] = auth_request.cookies['SS-SSO-LOGIN']


# Commit the pipeline
pipeline_endpoint = sch_url + '/pipelinestore/rest/v1/pipelines'

with open(path_to_pipeline, 'r', encoding='utf-8') as input_file:
    pipeline_json = json.load(input_file)

payload = {}
payload['name'] = pipeline_json['pipelineConfig']['title']
payload['commitMessage'] = commit_message
payload['pipelineDefinition'] = json.dumps(pipeline_json['pipelineConfig'])
payload['libraryDefinitions'] = json.dumps(pipeline_json['libraryDefinitions'])
payload['rulesDefinition'] = json.dumps(pipeline_json['pipelineRules'])

response = requests.put(url=pipeline_endpoint, headers=api_headers, json=payload)

if response.status_code != 201:
    print('Error committing pipeline')
    print(response.status_code)
    print(response.text)
    quit(-1)


# Write out the new pipeline metadata
remote_pipeline = response.json()

pipelineDefinition = json.loads(remote_pipeline['pipelineDefinition'])
rulesDefinition = json.loads(remote_pipeline['currentRules']['rulesDefinition'])

newMetadata = pipelineDefinition['metadata']
newMetadata['lastConfigId'] = pipelineDefinition['uuid']
newMetadata['lastRulesId'] = rulesDefinition['uuid']

with open(path_to_commit_metadata, 'w') as outfile:
    json.dump(newMetadata, outfile)

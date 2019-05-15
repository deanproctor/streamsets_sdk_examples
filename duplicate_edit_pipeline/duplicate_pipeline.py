#!/usr/bin/env python

from streamsets.sdk import ControlHub

sch_url = 'https://cloud.streamsets.com'
sch_user = 'user@org'
sch_pass = 'mypassword123'

sch = ControlHub(sch_url, username=sch_user, password=sch_pass)

pipeline = sch.pipelines.get(name='myPipeline')

builder = sch.get_pipeline_builder()
builder.add_error_stage('Discard')
new_pipeline = builder.build()

pipeline_definition = pipeline._pipeline_definition
pipeline_stages = pipeline.stages
pipeline_definition['title'] = 'myNewPipeline'
pipeline_definition['stages'] = []
for stage in pipeline_stages:
    pipeline_definition['stages'].append(stage._data)
new_pipeline._pipeline_definition = pipeline_definition
new_pipeline._data['pipeline_definition'] = pipeline_definition

sch.publish_pipeline(new_pipeline, 'My New Commit Message')

#!/usr/bin/env python

from streamsets.sdk import ControlHub

sch_url = 'https://cloud.streamsets.com'
sch_user = 'user@org'
sch_pass = 'mypassword123'

sch = ControlHub(sch_url, username=sch_user, password=sch_pass)

pipeline = sch.pipelines.get(name='myPipeline')

dev_stage = pipeline.stages.get(label='Dev Data Generator 1')
dev_stage.delay_between_batches = 10

sch.publish_pipeline(pipeline, 'My Commit Message')

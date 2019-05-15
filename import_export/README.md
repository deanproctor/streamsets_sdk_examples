Demonstrates how to programmatically manage import/export of StreamSets pipelines from an unregistered Data Collector to Control Hub.

## End-to-end usage:

### Initial commit:
* User exports pipeline, saves to "pipeline.json" for this example
* Import commit to Control Hub: python commit_pipeline.py pipeline.json "my first commit" metadata.json
* metadata.json contains the Control Hub metadata required to continue editing the pipeline in Data Collector

### Additional edits:
* Import the pipeline and apply the Control Hub metadata: python import_pipeline.py pipeline.json metadata.json
* User makes another change and exports updated pipeline, saves to "pipeline_v2.json"
* Import commit to Control Hub: python commit_pipeline.py pipeline_v2.json "my second commit" metadata.json
* metadata.json contains the Control Hub metadata required to continue editing the pipeline in Data Collector


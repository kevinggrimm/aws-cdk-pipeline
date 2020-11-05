#!/usr/bin/env python3

from aws_cdk import core

from pipeline_demo.pipeline_demo_stack import PipelineDemoStack
from pipeline_demo.pipeline_stack import PipelineStack


env_DEV = core.Environment(account="893961191302", region="us-west-1")

app = core.App()

PipelineDemoStack(app, "pipeline-demo")
PipelineStack(app, 'PipelineStack', env=env_DEV)

app.synth()

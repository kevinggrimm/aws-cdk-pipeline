from aws_cdk import core 
from pipeline_demo.pipeline_demo_stack import PipelineDemoStack

# TIP - Breaks tests out into three stages
# Given set, when this is tested, code asserts that the right event happens
# Adding the Stack to empty application, synthesizing the app; getting the Lambda function
# Testing the handler property has the right value

def test_lambda_handler():
  # GIVEN
  app = core.App()

  # WHEN 
  PipelineDemoStack(app, 'Stack')

  # THEN
  template = app.synth().get_stack_by_name('Stack').template
  functions = [resource for resource in template['Resources'].values() 
               if resource['Type'] == 'AWS::Lambda::Function']

  assert len(functions) == 1 
  assert functions[0]['Properties']['Handler'] == 'handler.handler'
from os import path

from aws_cdk import core
import aws_cdk.aws_lambda as lmb
import aws_cdk.aws_apigateway as apigw

class PipelineDemoStack(core.Stack):

    def __init__(self, scope: core.Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        # The code that defines your stack goes here
        this_dir = path.dirname(__file__)

        handler = lmb.Function(self, 'Handler',
            runtime=lmb.Runtime.PYTHON_3_7,
            handler='handler.handler',
            code=lmb.Code.from_asset(path.join(this_dir, 'lambda')))

        gw = apigw.LambdaRestApi(self, 'Gateway',
            description='Endpoint for a simple Lambda-powered web service',
            handler=handler.current_version)

        # Take the URL of the gateway; put it into a CloudFormation output
        # Allow you to get to the URL of the Lambda created earlier
        # Not in the code - when the code executes, there is nothing deployed
        # After it is created - later on in the pipeline - that URL will be known
        # and you can refer to it then
        self.url_output = core.CfnOutput(self, 'Url',
            value=gw.url)
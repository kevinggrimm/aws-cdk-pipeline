from aws_cdk import core

from .pipeline_demo_stack import PipelineDemoStack

class WebServiceStage(core.Stack):

    def __init__(self, scope: core.Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        service = PipelineDemoStack(self, 'WebService')

        # Reference the CFN Output from the stack
        self.url_output = service.url_output
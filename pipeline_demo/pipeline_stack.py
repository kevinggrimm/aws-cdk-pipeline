from aws_cdk import core

# Artifact - output of a codepipeline action and the input of a next one
# Will have a Source Artifact
# Build / synthesize step takes the source and produces a cloud assembly artifact (output of CDK application)
from aws_cdk import aws_codepipeline as codepipeline
from aws_cdk import aws_codepipeline_actions as cpactions
from aws_cdk import pipelines

from .webservice_stage import WebServiceStage

class PipelineStack(core.Stack):

    def __init__(self, scope: core.Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        source_artifact = codepipeline.Artifact()
        cloud_assembly_artifact = codepipeline.Artifact()

        # Install_command - installs CDK
        pipeline = pipelines.CdkPipeline(self, 'Pipeline', 
          cloud_assembly_artifact=cloud_assembly_artifact,
          pipeline_name='Webinar_Pipeline',

          source_action=cpactions.GitHubSourceAction(
            action_name='GitHub',
            output=source_artifact,
            oauth_token=core.SecretValue.secrets_manager('github-token'),
            owner='kevinggrimm',
            repo='aws-cdk-pipeline',
            trigger=cpactions.GitHubTrigger.POLL),

          synth_action=pipelines.SimpleSynthAction(
            source_artifact=source_artifact,
            cloud_assembly_artifact=cloud_assembly_artifact,
            install_command='npm install -g aws-cdk && pip install -r requirements.txt',
            synth_command='cdk synth')
        )

        # Can be a different account and region
        # As long as you have permissions it will work
        # Easy ability to deploy to different regions, accounts
        pipeline.add_application_stage(WebServiceStage(self, 'Pre-prod', 
          env=core.Environment(account="893961191302", region="us-west-1")))
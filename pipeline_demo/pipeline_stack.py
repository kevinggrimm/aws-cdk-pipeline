from aws_cdk import core

# Artifact - output of a codepipeline action and the input of a next one
# Will have a Source Artifact
# Build / synthesize step takes the source and produces a cloud assembly artifact (output of CDK application)
from aws_cdk import aws_codepipeline as codepipeline
from aws_cdk import aws_codepipeline_actions as cpactions
from aws_cdk import pipelines

class PipelineStack(core.Stack):

    def __init__(self, scope: core.Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        source_artifact = codepipeline.Artifact()
        cloud_assembly_artifact = codepipeline.Artifact()

        # Install_command - installs CDK
        pipelines.CdkPipeline(self, 'Pipeline', 
          cloud_assembly_artifact=cloud_assembly_artifact,
          pipeline_name='Webinar Pipeline',
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

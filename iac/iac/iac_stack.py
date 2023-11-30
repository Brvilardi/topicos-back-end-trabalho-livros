from aws_cdk import (
    # Duration,
    Duration,
    Stack,
    # aws_sqs as sqs,
    aws_lambda as lambda_

)
from constructs import Construct

class IacStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        self.lambda_layer = lambda_.LayerVersion(self, "LambdaLayer",
                                                 code=lambda_.Code.from_asset("../lambda_layer"),
                                                 compatible_runtimes=[lambda_.Runtime.PYTHON_3_9]
                                                 )
        
        self.enviar_feedback_lambda = lambda_.Function(self, "EnviarFeedbackLambda",
                                                         code=lambda_.Code.from_asset("../funcoes/enviar_feedback"),
                                                         handler="enviar_feedback_lambda.lambda_handler",
                                                         runtime=lambda_.Runtime.PYTHON_3_9,
                                                         timeout=Duration.seconds(30),
                                                         memory_size=128,
                                                         layers=[self.lambda_layer],
                                                         )

from aws_cdk import (
    # Duration,
    Duration,
    Stack,
    # aws_sqs as sqs,
    aws_lambda as lambda_,
    aws_dynamodb as dynamodb, RemovalPolicy

)

from aws_cdk.aws_apigateway import RestApi, Cors, LambdaIntegration

from constructs import Construct

from iac.front_stack import FrontEnd



class IacStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        ## ================== FrontEnd ================== ##

        self.front = FrontEnd(self, "FrontEnd")

        self.table = dynamodb.Table(
            self, "FeedbacksTable",
            partition_key=dynamodb.Attribute(
                name="PK",
                type=dynamodb.AttributeType.STRING
            ),
            billing_mode=dynamodb.BillingMode.PAY_PER_REQUEST,
            removal_policy=RemovalPolicy.DESTROY
        )

        ## ================== BACK ================== ##

        LAMBDA_ENVIRONMENTS = {
            "DYNAMO_TABLE": self.table.table_name,
        }

        ## ==== API Gateway ==== ##
        self.rest_api = RestApi(self, "FeedbacksAPI",
                                rest_api_name="FeedbacksAPI",
                                description="This is the RestApi for the FeedbacksAPI",
                                default_cors_preflight_options={
                                    "allow_origins": Cors.ALL_ORIGINS,
                                    "allow_methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
                                    "allow_headers": ["*"]
                                },
                                )

        self.api_gateway_resource = self.rest_api.root.add_resource("feedback", default_cors_preflight_options={
            "allow_origins": Cors.ALL_ORIGINS,
            "allow_methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
            "allow_headers": Cors.DEFAULT_HEADERS
        }
        )

        self.api_key = self.rest_api.add_api_key("FeedbacksAPIKey")

        self.api_usage_plan = self.rest_api.add_usage_plan("FeedbacksAPIUsagePlan",
                                                           name="FeedbacksAPIUsagePlan",
                                        throttle={
                                            "rate_limit": 10,
                                            "burst_limit": 1
                                        })
        
        self.api_usage_plan.add_api_stage(
            stage=self.rest_api.deployment_stage
        )
        
        self.api_usage_plan.add_api_key(self.api_key)
        
        

        ## ==== Lambdas ==== ##

        self.lambda_layer = lambda_.LayerVersion(self, "LambdaLayer",
                                                 code=lambda_.Code.from_asset(
                                                     "../lambda_layer"),
                                                 compatible_runtimes=[
                                                     lambda_.Runtime.PYTHON_3_9]
                                                 )

        self.enviar_feedback_lambda = lambda_.Function(self, "EnviarFeedbackLambda",
                                                       code=lambda_.Code.from_asset(
                                                           "../funcoes/enviar_feedback"),
                                                       handler="enviar_feedback_lambda.lambda_handler",
                                                       runtime=lambda_.Runtime.PYTHON_3_9,
                                                       timeout=Duration.seconds(
                                                           30),
                                                       memory_size=128,
                                                       layers=[
                                                           self.lambda_layer],
                                                        environment=LAMBDA_ENVIRONMENTS
                                                       )
        
        self.table.grant_read_write_data(self.enviar_feedback_lambda)

        self.api_gateway_resource.add_resource("enviar-feedback").add_method("POST",
                                                                             integration=LambdaIntegration(
                                                                                 self.enviar_feedback_lambda),
                                                                                 api_key_required=True)


        self.ler_feedback_lambda = lambda_.Function(self, "LerFeedbackLambda",
                                                         code=lambda_.Code.from_asset(
                                                              "../funcoes/ler_feedback"),
                                                         handler="ler_feedback_lambda.lambda_handler",
                                                         runtime=lambda_.Runtime.PYTHON_3_9,
                                                         timeout=Duration.seconds(
                                                              30),
                                                         memory_size=128,
                                                         layers=[
                                                              self.lambda_layer],
                                                          environment=LAMBDA_ENVIRONMENTS
                                                         )
        
        self.table.grant_read_write_data(self.ler_feedback_lambda)

        self.api_gateway_resource.add_resource("ler-feedback").add_method("GET",
                                                                                integration=LambdaIntegration(
                                                                                    self.ler_feedback_lambda),
                                                                                    api_key_required=True)

        self.ler_todos_feedbacks_lambda = lambda_.Function(self, "LerTodosFeedbacksLambda",
                                                            code=lambda_.Code.from_asset(
                                                                "../funcoes/ler_todos_feedbacks"),
                                                            handler="ler_todos_feedbacks_lambda.lambda_handler",
                                                            runtime=lambda_.Runtime.PYTHON_3_9,
                                                            timeout=Duration.seconds(
                                                                30),
                                                            memory_size=128,
                                                            layers=[
                                                                self.lambda_layer],
                                                            environment=LAMBDA_ENVIRONMENTS
                                                            )
        
        self.table.grant_read_write_data(self.ler_todos_feedbacks_lambda)

        self.api_gateway_resource.add_resource("ler-todos-feedbacks").add_method("GET",
                                                                                integration=LambdaIntegration(
                                                                                    self.ler_todos_feedbacks_lambda),
                                                                                    api_key_required=True)

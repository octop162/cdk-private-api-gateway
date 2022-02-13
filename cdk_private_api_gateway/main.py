from email import policy
from aws_cdk import (
    Stack,
    CfnOutput,
    aws_apigateway as apigateway,
    aws_ec2 as ec2,
    aws_iam as iam,
)

from constructs import Construct

from cdk_private_api_gateway.constant import Constant

class CdkPrivateApiGatewayStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # Load VPC
        vpc = ec2.Vpc.from_lookup(self, 'Vpc',
                                vpc_id=Constant.VPC_ID
                                )

        
        # VPC Intervface Endpoint
        vpc_endpoint = ec2.InterfaceVpcEndpoint(self, "VPCEncpointForAPIGateway",
                                vpc=vpc,
                                service=ec2.InterfaceVpcEndpointService('com.amazonaws.ap-northeast-1.execute-api'),
                                subnets=ec2.SubnetSelection()
                            )

        # Resource Policy
        policy = iam.PolicyDocument(
            statements=[
                iam.PolicyStatement(
                    effect=iam.Effect.ALLOW,
                    principals=[iam.AnyPrincipal()],
                    actions=['execute-api:Invoke'],
                    resources=['execute-api:/*'],
                ),
                iam.PolicyStatement(
                    effect=iam.Effect.DENY,
                    principals=[iam.AnyPrincipal()],
                    actions=['execute-api:Invoke'],
                    resources=['execute-api:/*'],
                    conditions={
                        'StringNotEquals': {
                            'aws::SourceVpc': Constant.VPC_ID,
                        }
                    }
                ),
            ]
        )

        # API gateway
        api = apigateway.RestApi(
            self,
            'SampleAPIGateway',
            endpoint_configuration=apigateway.EndpointConfiguration(
                types=[
                    apigateway.EndpointType.PRIVATE
                ],
                vpc_endpoints=[
                    vpc_endpoint
                ]
            ),
            policy=policy,
        )
        book_resource = api.root.add_resource("books")
        mock_integration = apigateway.MockIntegration(
            request_templates={
                'application/json': '{ "statusCode": 200 }'
            },
            passthrough_behavior=apigateway.PassthroughBehavior.WHEN_NO_TEMPLATES,
            integration_responses=[
                apigateway.IntegrationResponse(
                    status_code="200",
                    response_templates={
                        'application/json': '{ "statusCode": 200 }'
                    }
                )
            ],
        )
        book_resource.add_method("GET", mock_integration,
            method_responses=[apigateway.MethodResponse(status_code="200")]
        )
        

        CfnOutput(self, "URL",
            value=f"https://{api.rest_api_id}.execute-api.{self.region}.amazonaws.com/prod/books"
        )

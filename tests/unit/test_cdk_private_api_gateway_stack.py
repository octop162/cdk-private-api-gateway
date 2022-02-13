import aws_cdk as core
import aws_cdk.assertions as assertions

from cdk_private_api_gateway.cdk_private_api_gateway_stack import CdkPrivateApiGatewayStack

# example tests. To run these tests, uncomment this file along with the example
# resource in cdk_private_api_gateway/cdk_private_api_gateway_stack.py
def test_sqs_queue_created():
    app = core.App()
    stack = CdkPrivateApiGatewayStack(app, "cdk-private-api-gateway")
    template = assertions.Template.from_stack(stack)

#     template.has_resource_properties("AWS::SQS::Queue", {
#         "VisibilityTimeout": 300
#     })

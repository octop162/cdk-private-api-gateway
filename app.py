#!/usr/bin/env python3
import os

import aws_cdk as cdk

from cdk_private_api_gateway.constant import Constant
from cdk_private_api_gateway.main import CdkPrivateApiGatewayStack
from cdk_private_api_gateway.network import CdkPrivateApiGatewayNetworkStack


app = cdk.App()

CdkPrivateApiGatewayNetworkStack(app, "CdkPrivateApiGatewayNetworkStack")
CdkPrivateApiGatewayStack(app, "CdkPrivateApiGatewayStack", env=Constant.ACCOUNT_ENV)

app.synth()

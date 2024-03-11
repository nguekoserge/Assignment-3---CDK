#!/usr/bin/env python3
import os

import aws_cdk as cdk

from cam.cam_stack import ServerStack
from cam.cam_stack import NetworkStack

app = cdk.App()

network_stack = NetworkStack(app, "NetworkStack")
vpc = network_stack.vpc

# Utilisez-la lors de la création de ServerStack
ServerStack(app, "ServerStack", vpc=vpc)

app.synth()  


from aws_cdk import (
    # Duration,
    Stack,
    # aws_sqs as sqs,
)
from aws_cdk.aws_ec2 import Vpc, SubnetType, Instance, InstanceType, SecurityGroup, Peer, Port ,AmazonLinuxGeneration , AmazonLinuxImage , SubnetSelection
from aws_cdk.aws_rds import DatabaseInstance, DatabaseInstanceEngine, SubnetGroup
from constructs import Construct

class NetworkStack(Stack):
    def __init__(self, scope:Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)
        
        # Création du VPC
        self.vpc = Vpc(self, "MyVpc",
            cidr="10.0.0.0/16",
            max_azs=2, # Utilisez 2 zones de disponibilité
            subnet_configuration=[
                {"cidrMask": 24, "name": "Public", "subnetType": SubnetType.PUBLIC},
                {"cidrMask": 24, "name": "Private", "subnetType": SubnetType.PRIVATE_ISOLATED}
            ]
        )

class ServerStack(Stack):
    def __init__(self, scope:Construct, construct_id: str, vpc: Vpc, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)
        

        # Création des groupes de sécurité
    
        web_server_sg = SecurityGroup(self, "WebServerSG",
            vpc=vpc,
            allow_all_outbound=True
        )
        web_server_sg.add_ingress_rule(Peer.any_ipv4(), Port.tcp(80), "Allow inbound HTTP traffic")

        rds_sg = SecurityGroup(self, "RDSSG",
            vpc=vpc,
            allow_all_outbound=True
        )
        rds_sg.add_ingress_rule(web_server_sg, Port.tcp(3306), "Allow MySQL traffic from web servers")

        for idx, subnet in enumerate(vpc.public_subnets):
            instance_name = f"WebServer{idx + 1}"
            web_server = Instance(self, instance_name,
                instance_type=InstanceType("t2.micro"),
                machine_image=AmazonLinuxImage(generation=AmazonLinuxGeneration.AMAZON_LINUX_2),
                vpc=vpc,
                vpc_subnets=SubnetSelection(subnet_type=SubnetType.PUBLIC),
                security_group=web_server_sg
        )



            
        # Création de l'instance RDS dans les sous-réseaux privés
        rds_instance = DatabaseInstance(self, "MyRDS",
            engine=DatabaseInstanceEngine.MYSQL,
            vpc=vpc,
            vpc_subnets=SubnetSelection(subnet_type=SubnetType.PRIVATE_ISOLATED),  # Utilisation de vpc_subnets pour spécifier les sous-réseaux privés
            security_groups=[rds_sg]
        )






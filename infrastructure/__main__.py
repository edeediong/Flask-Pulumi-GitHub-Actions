"""A Python Pulumi program"""

import pulumi
import pulumi_aws as aws

user_data = """#!/bin/bash
sudo apt update -y
sudo apt install -y ruby
sudo apt-get install -y wget

# Install CodeDeploy for CICD
cd /home/ubuntu
wget https://aws-codedeploy-us-east-2.s3.amazonaws.com/latest/install
chmod +x ./install
sudo ./install auto
sudo service codedeploy-agent start
sudo apt update -y
sudo apt install -y python3-pip python3-dev build-essential libssl-dev libffi-dev python3-setuptools
sudo apt install -y python3-venv
sudo apt install -y nginx
sudo rm /etc/nginx/sites-enabled/default
sudo usermod -aG www-data ubuntu

"""

ec2_role = aws.iam.Role(
    "ec2_role",
    assume_role_policy="""{
        "Version":"2012-10-17",
        "Statement": [
            {
                "Effect":"Allow",
                "Principal": {
                    "Service":"ec2.amazonaws.com"
                    },
                    "Action":"sts:AssumeRole"
                }
            ]
        }""",
    description="Allows EC2 instances to call AWS services on your behalf.",
    force_detach_policies=False,
    max_session_duration=3600,
    name="CodeDeployInstanceRole",
    path="/",
    tags={"Name": "CodeDeployEC2",},
)

instance_profile = aws.iam.InstanceProfile("instance_profile",
    name="CodeDeployInstanceRole",
    path="/",
    role=ec2_role.name,
)

role_attach = aws.iam.RolePolicyAttachment("role_attach",
    policy_arn="arn:aws:iam::aws:policy/service-role/AmazonEC2RoleforAWSCodeDeploy",
    role=ec2_role.name,
)

role_attach_1 = aws.iam.RolePolicyAttachment("role_attach_1",
    policy_arn="arn:aws:iam::aws:policy/service-role/AutoScalingNotificationAccessRole",
    role=ec2_role.name,
)

codedeploy = aws.iam.Role(
    "codedeploy",
    assume_role_policy="""{
        "Version":"2012-10-17",
        "Statement": [
            {
                "Sid":"",
                "Effect":"Allow",
                "Principal": {
                    "Service":"codedeploy.amazonaws.com"
                    },
                    "Action":"sts:AssumeRole"
                }
            ]
        }""",
    description="Allows CodeDeploy to call AWS services such as Auto Scaling on your behalf.",
    force_detach_policies=False,
    max_session_duration=3600,
    name="CodeDeployServiceRole",
    path="/",
    tags={"Name": "CodeDeployEC2Service",},
)

codedeploy_attach = aws.iam.RolePolicyAttachment("codedeploy_attach",
    policy_arn="arn:aws:iam::aws:policy/service-role/AWSCodeDeployRole",
    role=codedeploy.name,
)

elb_sg = aws.ec2.SecurityGroup("elb_sg",
    description="launch-wizard-2 for aws instance firewalls",
    name="launch-wizard-2",
    revoke_rules_on_delete=False,
    tags={
        "Name": "AccureFlask",
    },
)

ingress = aws.ec2.SecurityGroupRule("ingress",
    cidr_blocks=["0.0.0.0/0"],
    from_port=80,
    protocol="tcp",
    security_group_id=elb_sg.id,
    self=False,
    to_port=80,
    type="ingress",
)

ingress_1 = aws.ec2.SecurityGroupRule("ingress_1",
    cidr_blocks=["0.0.0.0/0"],
    from_port=22,
    protocol="tcp",
    security_group_id=elb_sg.id,
    self=False,
    to_port=22,
    type="ingress",
)

egress = aws.ec2.SecurityGroupRule(
    "egress",
    from_port=0,
    to_port=0,
    protocol="-1",
    security_group_id=elb_sg.id,
    self=False,
    cidr_blocks=["0.0.0.0/0"],
    type="egress"
)

web = aws.ec2.Instance("web",
    ami="ami-0dd9f0e7df0f0a138",
    get_password_data=False,
    iam_instance_profile=ec2_role.name,
    instance_type="t2.micro",
    vpc_security_group_ids=[elb_sg.id],
    source_dest_check=True,
    key_name="flaskpulumi",
    tags={
        "Name": "FlaskPulumi",
    },
    user_data=user_data,
)

bucket = aws.s3.Bucket("bucket",
    acl="private",
    bucket="accure-codedeploy-deployment",
    force_destroy=True,
)

appname = aws.codedeploy.Application("appname",
    compute_platform="Server",
    name="aws-codedeploy",
)

deploy_group = aws.codedeploy.DeploymentGroup("deploy_group",
    app_name=appname.name,
    deployment_config_name="CodeDeployDefault.AllAtOnce",
    deployment_group_name="accure-test",
    ec2_tag_sets=[aws.codedeploy.DeploymentGroupEc2TagSetArgs(
        ec2_tag_filters=[{
            "key": "Name",
            "type": "KEY_AND_VALUE",
            "value": "FlaskPulumi",
        }],
    )],
    service_role_arn=codedeploy.arn,
)

pulumi.export("public_ip", web.public_ip)

"""A Python Pulumi program"""

import pulumi
import pulumi_aws as aws

user_data = """
#!/bin/bash
sudo apt-get update -y
sudo apt-get install -y ruby
sudo apt-get install -y wget
cd /home/ubuntu
wget https://bucket-name.s3.region-identifier.amazonaws.com/latest/install
chmod +x ./install
sudo ./install auto
sudo apt update -y
sudo apt install -y python3-pip python3-dev build-essential libssl-dev libffi-dev python3-setuptools
sudo apt install -y python3-venv
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

web = aws.ec2.Instance("web",
    ami="ami-0dd9f0e7df0f0a138",
    get_password_data=False,
    iam_instance_profile=ec2_role.name,
    instance_type="t2.micro",
    source_dest_check=True,
    key_name="flaskpulumi",
    tags={
        "Name": "FlaskPulumi",
    },
    user_data=user_data,
    )

elb_sg = aws.ec2.SecurityGroup("elb_sg",
    description="launch-wizard-2 for aws instance firewalls",
    name="launch-wizard-2",
    revoke_rules_on_delete=False,
    ingress=[aws.ec2.SecurityGroupIngressArgs(
        protocol="tcp",
        from_port=5000,
        to_port=5000,
        cidr_blocks=["0.0.0.0/0"]
        ),
        aws.ec2.SecurityGroupIngressArgs(
            protocol="tcp",
            from_port=22,
            to_port=22,
            cidr_blocks=["0.0.0.0/0"]
        ),
    ],
    tags={
        "Name": "AccureFlask",
    },
)

# volume_id = aws.ebs.Volume("volume_id",
#     availability_zone="us-east-2b",
#     tags={
#         "Name": "FlaskPulumi",
#     },
# )

# ebs = aws.ec2.VolumeAttachment("ebs",
#     device_name="/dev/sda1",
#     instance_id=web.id,
#     volume_id=volume_id.id,
# )

bucket = aws.s3.Bucket("bucket",
    acl="private",
    bucket="accure-codedeploy-deployment",
    force_destroy=False,
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

# g_actions = aws.iam.User(
#     "g_actions",
#     force_destroy=False,
#     name="accure-codedeploy",
#     path="/",
#     tags={
#         "Name": "GitHub-Actions-User",
#     },
# )

# user_attach = aws.iam.UserPolicyAttachment(
#     "user_attach",
#     policy_arn="arn:aws:iam::aws:policy/AmazonS3FullAccess",
#     user="accure-codedeploy",
# )

# user_attach_1 = aws.iam.UserPolicyAttachment(
#     "user_attach_1",
#     policy_arn="arn:aws:iam::aws:policy/AWSCodeDeployDeployerAccess",
#     user="accure-codedeploy",
# )

# g_actions_access_key = aws.iam.AccessKey(
#     "g_actions_access",
#     user=g_actions.name,
#     pgp_key="keybase:some_person_that_exists"
# )

# pulumi.export("secret_access_key_id", g_actions_access_key.id)
# pulumi.export("secret", g_actions_access_key.encrypted_secret)
pulumi.export("public_ip", web.public_ip)

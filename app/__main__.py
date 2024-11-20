import pulumi
import pulumi_aws as aws

# Configuration
ami_id = aws.ec2.get_ami(
    filters=[{"name": "name", "values": ["ubuntu/images/hvm-ssd/ubuntu-focal-20.04-amd64-server-*"]}],
    owners=["099720109477"],  # Canonical (Ubuntu) owner ID
    most_recent=True,
).id

instance_type = "t2.micro"
key_name = "my-key-pair"  # Replace with your AWS EC2 key pair name
vpc_id = "vpc-06af2864e8eab2b52"  # Replace with your VPC ID
subnet_id = "subnet-08a6f909284c5a5e8"  # Replace with a subnet ID in the VPC

# Security group for SSH and HTTP
security_group = aws.ec2.SecurityGroup(
    "gpu-cluster-sg",
    vpc_id=vpc_id,
    description="Allow SSH and HTTP",
    ingress=[
        {"protocol": "tcp", "from_port": 22, "to_port": 22, "cidr_blocks": ["0.0.0.0/0"]},  # SSH
        {"protocol": "tcp", "from_port": 80, "to_port": 80, "cidr_blocks": ["0.0.0.0/0"]},  # HTTP
    ],
    egress=[{"protocol": "-1", "from_port": 0, "to_port": 0, "cidr_blocks": ["0.0.0.0/0"]}],
)

# Create three t4g.micro EC2 instances
instances = []
for i in range(3):  # Create 3 instances
    instance = aws.ec2.Instance(
        f"t4g-instance-{i}",
        ami=ami_id,
        instance_type=instance_type,
        key_name=key_name,
        subnet_id=subnet_id,
        vpc_security_group_ids=[security_group.id],
        tags={
            "Name": f"t4g-instance-{i}",
            "Cluster": "t4g-cluster",
        },
    )
    instances.append(instance)

# Export public IPs
pulumi.export("instance_public_ips", [instance.public_ip for instance in instances])
pulumi.export("instance_ids", [instance.id for instance in instances])

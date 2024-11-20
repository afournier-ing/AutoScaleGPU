# AWS VPC and Subnet Creation via CLI

This guide demonstrates how to create a custom VPC and a subnet in AWS using the AWS CLI.

---

## Prerequisites

1. **AWS CLI Installed**: [Installation Guide](https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html)
2. **AWS CLI Configured**: Ensure your credentials are set up. Run:
   ```bash
   aws configure

    IAM Permissions:
        ec2:CreateVpc
        ec2:CreateSubnet
        ec2:CreateInternetGateway
        ec2:AttachInternetGateway
        ec2:ModifyVpcAttribute
        ec2:ModifySubnetAttribute

Steps
1. Create a VPC

aws ec2 create-vpc --cidr-block 10.0.0.0/16 --tag-specifications 'ResourceType=vpc,Tags=[{Key=Name,Value=MyVPC}]'

    Replace 10.0.0.0/16 with your desired CIDR block.
    Note the VpcId in the output.

2. Enable DNS Support and Hostnames (Optional)

aws ec2 modify-vpc-attribute --vpc-id <VpcId> --enable-dns-support '{"Value":true}'
aws ec2 modify-vpc-attribute --vpc-id <VpcId> --enable-dns-hostnames '{"Value":true}'

3. Create an Internet Gateway (Optional)

aws ec2 create-internet-gateway --tag-specifications 'ResourceType=internet-gateway,Tags=[{Key=Name,Value=MyInternetGateway}]'
aws ec2 attach-internet-gateway --internet-gateway-id <InternetGatewayId> --vpc-id <VpcId>

4. Create a Subnet

aws ec2 create-subnet --vpc-id <VpcId> --cidr-block 10.0.1.0/24 --availability-zone us-east-1a --tag-specifications 'ResourceType=subnet,Tags=[{Key=Name,Value=MySubnet}]'

    Replace 10.0.1.0/24 with your desired CIDR block.

5. Enable Public IPs for Subnet (Optional)

aws ec2 modify-subnet-attribute --subnet-id <SubnetId> --map-public-ip-on-launch

Outputs

    VPC ID: The identifier for your VPC.
    Subnet ID: The identifier for your subnet.
    Internet Gateway ID: (Optional) If created, this enables internet access.

Cleaning Up

To delete the resources:

    Detach and delete the internet gateway (if created):

aws ec2 detach-internet-gateway --internet-gateway-id <InternetGatewayId> --vpc-id <VpcId>
aws ec2 delete-internet-gateway --internet-gateway-id <InternetGatewayId>

Delete the subnet:

aws ec2 delete-subnet --subnet-id <SubnetId>

Delete the VPC:

    aws ec2 delete-vpc --vpc-id <VpcId>

References

    AWS CLI VPC Documentation
    AWS CLI Subnet Documentation


---

This README explains how to create, configure, and clean up a VPC and subnet using the AWS 



Create a New Key Pair

If the key pair doesn’t exist, you need to create one:
Option 1: Automatically Generate a Key Pair

Run the following command to create a new key pair and download the private key:

aws ec2 create-key-pair --key-name my-key-pair --query 'KeyMaterial' --output text > my-key-pair.pem

    Key Material: This saves the private key to a file named my-key-pair.pem.
    Permissions: Secure the private key file:

    chmod 400 my-key-pair.pem

Option 2: Import an Existing Public Key

If you already have an SSH key, you can upload the public key to AWS:

aws ec2 import-key-pair --key-name my-key-pair --public-key-material fileb://~/.ssh/id_rsa.

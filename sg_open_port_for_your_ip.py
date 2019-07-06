# Script will accept security group id and will open
# port for your public ip only
import sys
import boto3
import urllib.request
from botocore.exceptions import ClientError

if len(sys.argv) < 2:
    sys.exit("please provide security group id")

security_group_id = sys.argv[1]
print(security_group_id)

ec2 = boto3.client('ec2')


external_ip = urllib.request.urlopen('https://ident.me').read().decode('utf8')
print(external_ip)

try:

    data = ec2.authorize_security_group_ingress(
        GroupId=security_group_id,
        IpPermissions=[
            {'IpProtocol': 'tcp',
             'FromPort': 80,
             'ToPort': 80,
             'IpRanges': [{'CidrIp': external_ip+'/32','Description':'Allow Http traffic from my IP'}]},
            {'IpProtocol': 'tcp',
             'FromPort': 22,
             'ToPort': 22,
             'IpRanges': [{'CidrIp': external_ip+'/32','Description':'Allow SSH from my IP'}]}
        ])
    print('Ingress Successfully Set %s' % data)
except ClientError as e:
    print(e)

# Code
from distutils import command
import boto3
import time
import paramiko
import requests
import schedule

ec2_resource = boto3.resource('ec2')
ec2_client = boto3.client('ec2')

# For the distribution to be installed
image_id = 'ami-0122fd36a4f50873a'

# The name of the key under ec2/key pairs that can be used for connection
key_name = 'docker-server'
instance_type = 't2.small'
instance_name = 'my-server'

# the pem file must have restricted 400 permissions: chmod 400 absolute-path/boto3-server-key.pem
ssh_privat_key_path = '/home/arsha/.ssh/docker-server.pem' 
ssh_user = 'ec2-user'

def startEC2InstanceInDefaultVPS():
    # check if we have already created this instance using instance name
    response = ec2_client.describe_instances(
        Filters=[
            {
                'Name': 'tag:Name',
                'Values': [
                    f"{instance_name}",
                ]
            },
        ]
    ) 

    instance_already_exists = len(response["Reservations"]) != 0 and len(response["Reservations"][0]["Instances"]) != 0
    instance_id = ""

    if not instance_already_exists: 
        print("Creating a new ec2 instance")
        ec2_creation_result = ec2_resource.create_instances(
            ImageId=image_id, 
            KeyName=key_name, 
            MinCount=1, 
            MaxCount=1, 
            InstanceType=instance_type,
            TagSpecifications=[
                {
                    'ResourceType': 'instance',
                    'Tags': [
                        {
                            'Key': 'Name',
                            'Value': f"{instance_name}"
                        },
                    ]
                },
            ],

        )
        instance = ec2_creation_result[0]
        instance_id = instance.id
    else:
        instance = response["Reservations"][0]["Instances"][0]
        instance_id = instance["InstanceId"]
        print("Instance already exists")

    # Wait until the EC2 server is fully initialized
    ec2_instance_fully_initialized = False

    while not ec2_instance_fully_initialized:
        print("Getting instance status")
        statuses = ec2_client.describe_instance_status(
            InstanceIds = [instance_id]
        )
        if len(statuses['InstanceStatuses']) != 0:
            ec2_status = statuses['InstanceStatuses'][0]

            ins_status = ec2_status['InstanceStatus']['Status']
            sys_status = ec2_status['SystemStatus']['Status']
            state = ec2_status['InstanceState']['Name']
            ec2_instance_fully_initialized = ins_status == 'ok' and sys_status == 'ok' and state == 'running'
        if not ec2_instance_fully_initialized:
            print("waiting for 30 seconds")
            time.sleep(30)

    print("Instance fully initialized")


def retrievePublicIP():
    response = ec2_client.describe_instances(
        Filters=[
            {
                'Name': 'tag:Name',
                'Values': [
                    f"{instance_name}",
                ]
            },
        ]
    ) 
    instance = response["Reservations"][0]["Instances"][0]
    ssh_host = instance["PublicIpAddress"]
    print(f"public ip: {ssh_host}")
    return ssh_host


def installDockerAndNginx():
    commands_to_execute = [
        'sudo yum update -y && sudo yum install -y docker',
        'sudo systemctl start docker',
        'sudo usermod -aG docker ec2-user',
        'docker run -d -p 8080:80 --name nginx nginx'
    ]

    # connect to EC2 server
    print("Connecting to the server")
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(hostname=ssh_host, username=ssh_user, key_filename=ssh_privat_key_path)

    # install docker & start nginx 
    for command in commands_to_execute:
        stdin, stdout, stderr = ssh.exec_command(command)
        print(stdout.readlines())

    ssh.close()


def openPort8080OnNginx():
    sg_list = ec2_client.describe_security_groups(
        GroupNames=['default']
    )

    port_open = False
    for permission in sg_list['SecurityGroups'][0]['IpPermissions']:
        print(permission)
        # some permissions don't have FromPort set
        if 'FromPort' in permission and permission['FromPort'] == 8080:
            port_open = True

    if not port_open:
        sg_response = ec2_client.authorize_security_group_ingress(
            FromPort=8080,
            ToPort=8080,
            GroupName='default',
            CidrIp='0.0.0.0/0',
            IpProtocol='tcp'
        )

# Scheduled function to check nginx application status and reload if not OK 5x in a row
app_not_accessible_count = 0

def restart_container():
    print('Restarting the application...')
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(hostname=ssh_host, username=ssh_user, key_filename=ssh_privat_key_path)
    stdin, stdout, stderr = ssh.exec_command('docker start nginx')
    print(stdout.readlines())
    ssh.close()
    # reset the count
    global app_not_accessible_count
    app_not_accessible_count = 0
    
    print(app_not_accessible_count)


def monitor_application():
    global app_not_accessible_count
    try:
        response = requests.get(f"http://{ssh_host}:8080")
        if response.status_code == 200:
            print('Application is running successfully!')
        else:
            print('Application Down. Fix it!')
            app_not_accessible_count += 1
            if app_not_accessible_count == 5:
                restart_container()
    except Exception as ex:
        print(f'Connection error happened: {ex}')
        print('Application not accessible at all')
        app_not_accessible_count += 1
        if app_not_accessible_count == 5:
            restart_container()
        return "test"

startEC2InstanceInDefaultVPS()
ssh_host = retrievePublicIP()
installDockerAndNginx()
openPort8080OnNginx()
schedule.every(10).seconds.do(monitor_application)  

while True:
    schedule.run_pending()



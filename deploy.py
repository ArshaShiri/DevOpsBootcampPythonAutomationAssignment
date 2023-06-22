import paramiko

ssh_host = os.environ['EC2_SERVER']
ssh_user = os.environ['EC2_USER']
ssh_private_key = os.environ['AWS_SSH_KEY']

# SSH into the EC2 server
ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect(hostname=ssh_host, username=ssh_user, key_filename=ssh_private_key)

stdin, stdout, stderr = ssh.exec_command(f"pwd")
print(stdout.readlines())

ssh.close()


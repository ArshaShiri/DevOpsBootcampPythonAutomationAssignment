import paramiko

ssh_host = "3.121.196.12"
ssh_user = "ec2-user"

# Should be absolute path
ssh_private_key = "/home/arsha/Downloads/python-automation-assignment.pem"

# SSH into the EC2 server
ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect(hostname=ssh_host, username=ssh_user, key_filename=ssh_private_key)

stdin, stdout, stderr = ssh.exec_command(f"pwd")
print(stdout.readlines())

ssh.close()


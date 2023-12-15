import paramiko
import io

client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

def ssh_send(ip, private_key, command):
  client.connect(ip, username='root', pkey=paramiko.RSAKey.from_private_key(io.StringIO(private_key)))
  client.exec_command(command)

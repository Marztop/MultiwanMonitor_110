import paramiko
import time

class device:
    def __init__(self,hostname,port,username,password):
        self.hostname = hostname
        self.port = port
        self.username = username
        self.password = password
        self.client = paramiko.SSHClient()
        self.client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.client.connect(hostname=self.hostname, port=self.port, username=self.username, password=self.password)
        self.shell = self.client.invoke_shell()
    


    def send_command(self,command,prompt_time=0.2):
        self.shell.send('%s\n'%(command))
        time.sleep(prompt_time)
        output = self.shell.recv(65535).decode('ascii')
        return output



    def connect(self):
        self.client.connect(hostname=self.hostname, port=self.port, username=self.username, password=self.password)
        self.shell = self.client.invoke_shell()
    


    def close(self):
        self.client.close()
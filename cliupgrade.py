import paramiko
import time

# List of Commands to execute .... update the iterable below if running "commands1"
commands1 = ['shell\n', 'cd /var/nsinstall\n', 'mkdir newFirmware\n',
             'tar -xzvf /var/nsinstall/NSVPX-KVM-13.0-79.64_nc_64.tgz -C /var/nsinstall/newFirmware\n',
             'cd /var/nsinstall/newFirmware\n', 'installns -Y > nsupdate.log\n', 'reboot\n', 'N\n']

# List of Commands to execute .... update the iterable below if running "commands2"
commands2 = ['add service service-HTTP-1 10.10.50.5 HTTP 80\n', 'add service service-HTTP-2 10.10.50.15 HTTP 80\n',
             'add lb vserver vserver-LB-1 HTTP 10.10.2.60 80\n', 'add lb vserver vserver-LB-2 HTTP 10.10.2.70 80\n',
             'bind lb vserver vserver-LB-1 service-HTTP-1\n', 'bind lb vserver vserver-LB-2 service-HTTP-2\n',
             'show service bindings service-HTTP-1\n'
             ]

max_buffer = 65535


def connect_do_stuff(host, username, password, port):
    # Connect to to the hostname
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(hostname=host, username=username, password=password, port=port, look_for_keys=False, allow_agent=False)
    return ssh


def clear_buffer(connection):
    if connection.recv_ready():
        return connection.recv(max_buffer)


# Enter connection details here
connection = connect_do_stuff(host='172.20.10.10', username='nsroot', password='nsroot', port=22)

new_connect = connection.invoke_shell()
output = clear_buffer(new_connect)

#iterating over the command set you want to run - make sure to change the command set to the set you want to run. Change to "command1" if you intend to run the commands in the command1 list
for command in commands2:
    print(f".....Now executing command {command}")
    new_connect.send(command)
    time.sleep(10)
    output = new_connect.recv(max_buffer)
    # command output
    print(output)

# connection close
new_connect.close()

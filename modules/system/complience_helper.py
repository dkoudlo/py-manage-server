import os
import socket
import subprocess
import re
from contextlib import closing
from modules.file.file_helper import File

# this class manages complience of the system
# the complience is provided as a configuration 
# and is checked against the system its runnning on
# we can extend any playbook with options:
# the remediation functions offer particular fixes
class SystemComplience:

    # options passed in are defined as follows
    # 
    # config sample
    #   comply:
    #     - port_open: 80
    #     - disk_free_percent: 80
    #     - dns_resolves: 'http://192.21.21.12/'
    #     - hostname_resolves: ok


    # check if storage requirement is complient
    # remitigation
    # checks if theres enough virtual storage
    # checks physical storage
    # remediates  
    # sees if there are any delete files that could be cleaned
    def remediate_storage(self, disk_free_prcnt):
        # for now get the root FS stats
        # TODO: use os.stat instead
        st = os.statvfs('/')

        # block size * total blocks
        size = float(st.f_frsize * st.f_blocks)
        # block size * free blocks
        free = float(st.f_frsize * st.f_bfree)
        # block size * non-super user blocks available
        free_user = float(st.f_frsize * st.f_bavail)
        
        # total available
        available = free / size * 100.0
        # total available for normal os user
        usr_available = free_user / size * 100.0

        # run the command du -Psx /
        # shortcut instead of walking through all the dirs
        du = self.get_cmd_output('du', ['-Psx','/'] )
        du = du.split("\t")[0]

        # storage taken 
        du_bytes = int(du) * 1024 
        storage_available_prcent = (float(du) * 1024) / size * 100.0
        # total available for everyone

        if disk_free_prcnt > usr_available:
            print "Not enough User Space, only " + str(int(usr_available)) + "% of required " + str(int(disk_free_prcnt)) + "%"
            if disk_free_prcnt < available:
                print "There's enough logical space available for super-users: " + str(int(available)) + "% of required " + str(int(disk_free_prcnt)) + "%"
            else:
                print "Not enough logical space, only " + str(int(available)) + "% of required " + str(int(disk_free_prcnt))
                if disk_free_prcnt > storage_available_prcent:
                    print "Physical storage used: " + str(storage_available_prcent) + "%"            
                    
                    out = self.get_cmd_output('lsof', ['-nP','+L1'])
                    if len(out) > 1:
                        print "There's a deleted file(s) in memory, please try and kill process or truncate the file to regain space."
                        for line in out[1:len(out)-1]:
                            line = line.split()
                            print "Name/Pid 'File':  " + line[0] + "/" + line[1] + " '" + line[len(line)-2] + "'"
        else:
            print "There's enough user space avaialable: " + str(int(usr_available)) + "% is avaialable of required " + str(int(disk_free_prcnt)) + "%"
            

    # use to check external hostnames
    def remediate_dns(self, hostname):
        self.remediate_hostname_resolves(hostname)

    # use to check internal hostname
    # checks if NSS (Name Service Switch) is configured ok
    def remediate_hostname(self, option):
        if option == 'yes':
            print 'Trying to resolve '

        hostname = socket.gethostname()
        try:
            socket.gethostbyname(hostname)
            return 1
        except socket.gaierror:
            return 0
        finally:
            socket.close()

    # checks if the port is open or closed
    # if no process check firewall
    # check if the port availabe to bind to
    # if not see what process PID has it
    def remediate_port(self, port):
 
        # check if port is within range
        if port > 0 and port <= 65535:
            is_open = self.is_socket_open('127.0.0.1', port)
            is_bindable = self.is_socket_bindable(port)
            
            if is_open and is_bindable:
                print "Port is open and availabe for use: port " + str(port)
            else:
                if is_open:
                    print "Port is open for incoming connections: " + str(port)
                else:
                    print "Please see your firewall settings are correct and allow incoming connections on port: " + str(port)
                if not is_bindable:
                    print "Looks like port: " + str(port) + " is taken by another process."
                    # netstat -tulpn | grep --color :80
                    out = self.get_cmd_output('netstat', '-tulpn' )
                    # find port reference on line
                    pids_prog = set()
                    for line in out.split("\n"):
                        if line.find(":" + str(port)) > 0:
                            # remove multi space spaces and split by space
                            line = re.sub('\s\s+', ' ', line.strip()).split(" ")
                            pids_prog.add(line[len(line)-1])
                            print "socket state is: " + line[len(line)-2] + "\tfor protocol: " + line[0] + "\ton Local Address: " + line[3]
                    print "The port is taken by the PID/Program Name: " + ", ".join(pids_prog)
                    print "Please see if the process's above should be stoped first!"
        else:
            print 'The port is out of range: ' + port


    def get_cmd_output(self, command, switches):
        cmd = [command]
        # handle multiple swithes
        if isinstance(switches, list):
            for switch in switches:
                cmd = cmd + [switch]
        else:
            cmd = cmd + [switches]
        
        return subprocess.check_output(cmd)


    def is_socket_open(self, host, port):
        # make sure the socket gets closed afer check
        with closing(socket.socket(socket.AF_INET, socket.SOCK_STREAM)) as sock:
            # set timeout so it does not take too long to connect
            sock.settimeout(5.0)
            if sock.connect_ex((host, port)) == 0:
                return True
            else:
                return False

    def is_socket_bindable(self, port):
        with closing(socket.socket(socket.AF_INET, socket.SOCK_STREAM)) as sock:
            try:
                sock.bind(("127.0.0.1", port))
            except socket.error as err:
                if err.errno == 98:
                    return False
                else:
                    # something else raised the socket.error exception
                    return True

    # # ############### Not Used ####################
    # # check if file is complient
    # def check_file(self):
    #     os.path.isfile(fname)
        

    # # check if memory requirement is ok
    # # TODO: Not needed yet
    # def check_memory(self):
    #     """
    #     Get node total memory and memory usage
    #     """
    #     with open('/proc/meminfo', 'r') as mem:
    #         ret = {}
    #         tmp = 0
    #         for i in mem:
    #             sline = i.split()
    #             if str(sline[0]) == 'MemTotal:':
    #                 ret['total'] = int(sline[1])
    #             elif str(sline[0]) in ('MemFree:', 'Buffers:', 'Cached:'):
    #                 tmp += int(sline[1])
    #         ret['free'] = tmp
    #         ret['used'] = int(ret['total']) - int(ret['free'])
    #     return ret
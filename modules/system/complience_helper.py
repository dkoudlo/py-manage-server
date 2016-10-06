import os
import os.path
import socket
import subprocess
import re
from contextlib import closing
from modules.file.file_helper import File
# this class manages complience of the system
# the complience is provided as a configuration 
# and is checked against the system its runnning on
# we can extend any playbook with options:
# 
class SystemComplience:

    # options passed in are defined as follows
    # 
    # config sample
    #   comply:
    #     - port_open: 80
    #     - disk_free_percent: 80
    #     - dns_resolves: 'http://192.21.21.12/'
    #     - hostname_resolves: ok

    def __init__(self):
        # self.hostname = localhostname
        pass

    # get hostname from path
    def get_hostname(self):
        pass

    # check if storage requirement is complient
    # mitigation
    # check occupied space if 
    # if physical storage is ok, check for open files
    def mediate_storage(self, disk_free_prcnt):
        
        # for now get the root FS stats
        statvfs = os.statvfs('/')

        size = float(statvfs.f_frsize * statvfs.f_blocks)     # Size of filesystem in bytes
        free = float(statvfs.f_frsize * statvfs.f_bfree)      # Actual number of free bytes
        free_user = float(statvfs.f_frsize * statvfs.f_bavail)     # Number of free bytes that ordinary users have available
        
        available = free / size * 100.0
        usr_available = free_user / size * 100.0

        if disk_free_prcnt < available:
            print "There's enough physical space available: " + str(int(available)) + "% of required " + str(int(disk_free_prcnt)) + "%"
        else:
            print "Not enough physical space, only " + str(int(available)) + "%% of required " + str(int(disk_free_prcnt))
        
        if disk_free_prcnt > usr_available:
            print "Not enough User Space, only " + str(int(usr_available)) + "% of required " + str(int(disk_free_prcnt)) + "%"
        else:
            print "There's enough user space avaialable: " + str(int(usr_available)) + "% is avaialable of required " + str(int(disk_free_prcnt)) + "%"


    # use to check external hostnames
    def mediate_dns_resolves(self, hostname):
        self.hostname_resolves(hostname)

    # use to check internal hostname
    def mediate_hostname_resolves(self, option):
        if option == 'yes':
            print 'Trying to resolve '
        try:
            socket.gethostbyname(hostname)
            return 1
        except socket.error:
            return 0

    # checks if the port is open or closed
    # if no process check firewall
    # check if the port availabe to bind to
    # if not see what process PID has it
    def mediate_socket_connection(self, port):
 
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
                    out, err = self.get_cmd_output('netstat', '-tulpn' )
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
        
        prcss = subprocess.Popen(cmd, stdout=subprocess.PIPE,
                                      stderr=subprocess.PIPE)
        # return out, error
        return prcss.communicate()


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
import os
import os.path
import socket
from contextlib import closing
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
    #     - disk_free: 80% 
    #     - dns_resolves: 'http://192.21.21.12/'
    #     - hostname_resolves: ok

    def __init__(self, options):
        self.hostname = localhostname
        pass

    # get hostname from path
    def get_hostname(self):
        pass

    # check if storage requirement is complient
    # mitigation
    # check occupied space if 
    # if physical storage is ok, check for open files
    def check_storage(self):
        # for now get the root FS stats
        statvfs = os.statvfs('/')

        statvfs.f_frsize * statvfs.f_blocks     # Size of filesystem in bytes
        statvfs.f_frsize * statvfs.f_bfree      # Actual number of free bytes
        statvfs.f_frsize * statvfs.f_bavail     # Number of free bytes that ordinary users have available
        pass



    # use to check external hostnames
    def check_dns_resolves(hostname):
        hostname_resolves(hostname)

    # use to check internal hostname
    def hostname_resolves(self, hostname):
        try:
            socket.gethostbyname(hostname)
            return 1
        except socket.error:
            return 0


    # checks if the port is open or closed
    # check if the port availabe
    # if not see what process PID has it
    # if no process check firewall
    def check_socket(host, port):
        with closing(socket.socket(socket.AF_INET, socket.SOCK_STREAM)) as sock:
            if sock.connect_ex(('127.0.0.1', port)) == 0:
                print "Port is open"
            else:
                print "Port is not open"


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
import os
import socket
import subprocess
import re
import sys
from contextlib import closing
from modules.file.file_helper import File

# this class manages complience of the system
# the complience is provided as a configuration 
# and is checked against the system its runnning on
# we can extend any playbook with options:
# the remediation functions offer particular fixes
class DebianSystemComplience:

    # options passed in are defined as follows
    # 
    # config sample
    #   comply:
    #     - port_open: 80
    #     - disk_free_percent: 80
    #     - dns_ok: google.com
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
                    
                    # chck for unreleased files in memory
                    out = self.get_cmd_output('lsof', ['-nP','+L1'])
                    if len(out) > 1:
                        print "There's a deleted file(s) in memory, please try and kill process or truncate the file to regain space."
                        for line in out[1:len(out)-1]:
                            line = line.split()
                            print "Name/Pid 'File':  " + line[0] + "/" + line[1] + " '" + line[len(line)-2] + "'"
                    sys.exit("Fatal Complience Error: Not Enough Space")
        else:
            print "There's enough user space avaialable: " + str(int(usr_available)) + "% is avaialable of required " + str(int(disk_free_prcnt)) + "%"
            

    # use to check external hostnames
    # takes in FQDN hostname
    def remediate_dns(self, hostname):
        print "Trying to see if: " + hostname + " will resolve."
        try:
            ip = socket.gethostbyname(hostname)
            print "DNS reolved ok for host: " + hostname + " with IP: " + ip
        except socket.gaierror:
            # /etc/nsswitch.conf should contain dns method 
            # so Debian knows it should use one of the nameservers in the /etc/resolv.conf
            self.check_nsswitch_hosts_ok("dns")

            resolve_conf_nameserver = self.get_line_starts_with("/etc/resolv.conf", "nameserver")

            if resolve_conf_nameserver != "":
                nameserver_ip = resolve_conf_nameserver.split()[1]

                is_dns_port_open = self.is_socket_open(nameserver_ip, 53)
                if not is_dns_port_open:
                    print "Cannot Reach DNS server specified in the resolv.conf, please make sure it is not blocked by firewall."
                else:
                    print "Fatal complience error: DNS is not functinal."
                    print "- Please make sure it is not cached via local DNS proxy."
                    print "- Please check /etc/hosts for the " + hostname + " entrie."
                    sys.exit( "- Please make sure the hostname is complient with FQDN" )
            else:
                print "No nameserver definition found in the /etc/resolv.conf. Please fix."




    def remediate_hostname(self, option):
        # get hostname
        hostname = socket.gethostname()

        if option:
            print 'Trying to resolve hostname: ' + hostname
            try:
                # resolve hostneme to an ip
                socket.gethostbyname(hostname)
                print "Hostname resolution is OK"
            except socket.gaierror as err:
                # /etc/nsswitch.conf should contain file method
                nsswitch_ok = self.check_nsswitch_hosts_ok("file")
                # The files method is invoked first. If the hostname is found in 
                # the "/etc/hosts" file, it returns all valid addresses for it and 
                # exits.
                # check if default ip is ok
                # could be a different ip, but will use default Debian
                deflt_ip = "127.0.1.1"
                hosts_default_ip = self.get_line_starts_with("/etc/hosts", deflt_ip)
                deflt_ip_ok = False
                for word in hosts_default_ip.split():
                    if word == hostname:
                        print "/etc/hosts has " + deflt_ip + " " + hostname + " defined properly"
                        deflt_ip_ok = True
                        break

                if not deflt_ip_ok:
                    print "Fatal Complience Error: "
                    sys.exit( "Please make sure /etc/hosts has default ip entrie: " + deflt_ip + "\t" + hostname )
                else:
                    print "Could not find why hostname resolution did not work."
                    print "Please check:\n- /etc/hostname file is not empty"
                    print "- maybe hostname is cached on local proxy DNS server, etc."
        else:
            print "Will not check for hostname complience, the option is: " + str(option)

    # The "/etc/nsswitch.conf" file with stanza like "hosts: files dns" 
    # dictates the hostname resolution order.
    # returns if the method is found 
    def check_nsswitch_hosts_ok(self, method):
        # get the hosts: stanza
        nsswitch_hosts = self.get_line_starts_with("/etc/nsswitch.conf", "hosts")
        # should contain method
        for word in nsswitch_hosts.split():
            if word == method:
                print "/etc/nsswitch.conf config is OK and contains method " + method
                return True
        print "/etc/nsswitch.conf config does not have method " + method + " Please make sure hosts: stanza has proper method."
        return False

    # takes in regex pattern and path of the file
    # returns line from file and empty string is not found ""
    def get_line_starts_with(self, path, pattern):
        # open file for reading
        with open(path, "r") as f:
            for line in f:
                # find first occurience from begging of the file
                if re.match(pattern, line) != None:
                    return line
        return ""

    # checks if the port is open or closed
    # if no process check firewall
    # check if the port availabe to bind to
    # if not see what process PID has it
    def remediate_port(self, port):
 
        # check if port is within range
        if port > 0 and port <= 65535:
            # use lopback to check local machine
            is_open = self.is_socket_open('127.0.0.1', port)
            is_bindable = self.is_socket_bindable(port)
            
            if is_open and is_bindable:
                print "Port is open and availabe for use: port " + str(port)
            else:
                if is_open:
                    print "Port is open for incoming connections: " + str(port)
                else:
                    print "Please see your firewall settings are correct to allow incoming connections on port: " + str(port)
                if not is_bindable:
                    print "Looks like port: " + str(port) + " is taken by another process."
                    # netstat -tulpn | grep --color :80
                    out = self.get_cmd_output('netstat', '-tulpn' )
                    # find port reference on line
                    pids_prog = set()
                    for line in out.split("\n"):
                        if line.find(":" + str(port) + " ") > 0:
                            # remove multi space spaces and split by space
                            line = re.sub('\s\s+', ' ', line.strip()).split(" ")
                            pids_prog.add(line[len(line)-1])
                            print "socket state is: " + line[len(line)-2] + "\tfor protocol: " + line[0] + "\ton Local Address: " + line[3]
                    print "The port is taken by the PID/Program Name: " + ", ".join(pids_prog)
                    print "Warning Complience Error: Please see if the process's above should be stoped first!"
        else:
            print 'The port is out of range: ' + port + '. Please fix configuration'

    # run command and return output
    def get_cmd_output(self, command, switches):
        cmd = [command]
        # handle multiple swithes
        if isinstance(switches, list):
            for switch in switches:
                cmd = cmd + [switch]
        else:
            cmd = cmd + [switches]
        
        return subprocess.check_output(cmd)

    # check if socket is open
    def is_socket_open(self, host, port):
        # make sure the socket gets closed afer check
        with closing(socket.socket(socket.AF_INET, socket.SOCK_STREAM)) as sock:
            # set timeout so it does not take too long to connect
            sock.settimeout(5.0)
            if sock.connect_ex((host, port)) == 0:
                return True
            else:
                return False

    # check if we could use the socket on local machine
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

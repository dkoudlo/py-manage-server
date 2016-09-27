import subprocess
import sys

class SystemService:

    # constractor
    def __init__(self, service_name, sudo=False):
        self.name = service_name
        self.spids = self.get_current_pids()
        self.base_command = ["service", self.name]
        self.sudo = sudo

    # get set of pids for service name
    def get_current_pids(self):
        try:
            # using pgrep here, comes standard on debian distros
            return set(subprocess.check_output(["pgrep", self.name]).splitlines())
        except subprocess.CalledProcessError:
            # return empty set
            return set()

    # start service
    def start(self):
        # service has pids means already running
        if len(self.spids) > 0:
            print "Service [" + self.name + "] is running."
        else:
            print subprocess.check_output(self.make_service_command("start"))
            # update service pids
            self.spids = self.get_current_pids()

    # stop service
    def stop(self):
        # no pid lets start the service
        if len(self.spids) == 0:
            print "Service [" + self.name + "] is not running."
        else:
            print subprocess.check_output(self.make_service_command("stop"))
            # update service pids
            self.spids = self.get_current_pids()

    # restart service
    def restart(self):
        old_pids = self.spids
        
        self.stop()
        self.start()
        
        new_pids = self.spids

        # see if pids changed and service is running
        if old_pids not in new_pids and len(new_pids) > 0:
            print "Restarted: " + self.name
        else:
            # service did not stop lets kill all of its pids one more time
            if len(new_pids) > 0:
                for pid in new_pids:
                    subprocess.call(["pkill", "-9", self.name])
            # lets try and start it again
            self.start()
            if len(self.spids) > 0:
                print "Force restarted [" + self.name + "]."
            else:
                sys.exit("Fatal: Could not start service [" + self.name + "]. Please check if applied config is OK")

    # prepend sudo to the command
    def command_add_sudo(self, command_array):
        return ["sudo"] + command_array

    # create command return array
    def make_service_command(self, operation):
        if self.sudo :
            return self.command_add_sudo(self.base_command) + [operation]
        else:
            return self.base_command + [operation]
import subprocess
import sys

class SystemService:

    def __init__(self, service_name):
        self.name = service_name
        self.spids = self.get_current_pids()

    # get set of pids for service name
    def get_current_pids(self):
        try:
            return set(subprocess.check_output(["pgrep", self.name]).splitlines())
        except subprocess.CalledProcessError:
            return set()

    # start service
    def start(self):
        # service has pids means already running
        if len(self.spids) > 0:
            print "Service [" + self.name + "] is running."
        else:
            print subprocess.check_output(["service", self.name, "start"])
            # update service pids
            self.spids = self.get_current_pids()

    # stop service
    def stop(self):
        # no pid lets start the service
        if len(self.spids) == 0:
            print "Service [" + self.name + "] is not running."
        else:
            print subprocess.check_output(["service", self.name, "stop"])
            # update service pids
            self.spids = self.get_current_pids()


    def restart(self):
        old_pids = self.spids
        
        self.stop()
        self.start()
        
        new_pids = self.spids

        if old_pids not in new_pids and len(new_pids) > 0:
            print "Restarted: " + self.name
        else:
            # service did not stop lets kill it
            for pid in new_pids:
                subprocess.call(["pkill", self.name])
            # lets try and start it again
            self.start()
            if len(self.spids) > 0:
                print "Force restarted [" + self.name + "]."
            else:
                sys.exit("Fatal: Could not start service [" + self.name + "].")




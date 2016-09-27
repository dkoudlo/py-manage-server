import modules.options_helper
from modules.system.service_helper import SystemService 

def main(options):

    # available config keys
    options_registry = ["name","status","sudo"]

    # verify config option provided match registry
    modules.options_helper.check_options(options, options_registry)

    name = options.get("name", False)
    status = options.get("status", False)
    sudo = options.get("sudo", False)

    if name and status:
        sc = SystemService(name, sudo)
        if status == "restarted":
            sc.restart()
        elif status == "stopped":
            sc.stop()
        elif status == "running":
            sc.start()
        else:
            print "Service status is not supported: " + status
    else:
        print "Please check config"

if __name__ == '__main__':
    main(options)

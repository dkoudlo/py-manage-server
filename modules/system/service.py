import modules.options_helper
from modules.system.service_helper import SystemService 

def main(options):

    options_registry = ["name","status"]
    modules.options_helper.check_options(options, options_registry)

    name = options.get("name", False)
    status = options.get("status", False)

    print options

    if name and status:
        sc = SystemService(name)
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

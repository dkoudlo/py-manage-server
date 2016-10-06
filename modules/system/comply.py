import modules.options_helper
from modules.system.complience_helper import SystemComplience 

# this module runs complience checks and suggests remediations
def main(options):

    # available config keys
    options_registry = ["port_open","disk_free_percent","dns_resolves","hostname_resolves"]

    # verify config option provided match registry
    modules.options_helper.check_options(options, options_registry)

    # config sample
    #system:
    #   comply:
    #     - port_open: 80
    #     - disk_free_percent: 80
    #     - dns_resolves: 'http://192.21.21.12/'
    #     - hostname_resolves: ok
    port_open = options.get("port_open", False)
    disk_free_percent = options.get("disk_free_percent", False)
    dns_resolves = options.get("dns_resolves", False)
    hostname_resolves = options.get("hostname_resolves", False)
    
    if len(options) == 1:
        cmply = SystemComplience()
        if port_open:
            cmply.mediate_socket_connection(port_open)
        if disk_free_percent:
            cmply.mediate_storage(disk_free_percent)
        if dns_resolves:
            cmply.mediate_dns_resolves(dns_resolves)
        if hostname_resolves:
            cmply.mediate_hostname_resolves(hostname_resolves)
    else:
        print "Please configure one option in the list format: " + ", ".join(options_registryo)
        sys.exit("Example :\nsystem:\n    comply:\n        - option1\n        -option2")

if __name__ == '__main__':
    main(options)

import modules.options_helper
from modules.system.complience_helper import SystemComplience 

# this module runs complience checks and suggests remediations
def main(options):

    # available config keys
    options_registry = ["port_open","disk_free","dns_resolves","hostname_resolves"]

    # verify config option provided match registry
    modules.options_helper.check_options(options, options_registry)

    # config sample
    #   comply:
    #     - port_open: 80
    #     - disk_free: 80% 
    #     - dns_resolves: 'http://192.21.21.12/'
    #     - hostname_resolves: ok
    port_open = options.get("port_open", False)
    disk_free = options.get("disk_free", False)
    dns_resolves = options.get("dns_resolves", False)
    hostname_resolves = options.get("hostname_resolves", False)
    
    if port_open:
        pass
    if disk_free:
        pass
    if dns_resolves:
        pass
    if hostname_resolves == 'ok':
        pass
    else:
        print


if __name__ == '__main__':
    main(options)

import modules.options_helper
from modules.system.complience_helper import SystemComplience 

# this module runs complience checks and suggests remediations
def main(options):

    # available config keys
    options_registry = ["port_ok","disk_free_percent","dns_ok","hostname_ok"]

    # verify config option provided match registry
    modules.options_helper.check_options(options, options_registry)

    # config sample
    #system:
    #   comply:
    #     - port_ok: 80
    #     - disk_free_percent: 80
    #     # google.com is reachable
    #     - dns_ok: 'googl.com'
    #     - hostname_ok: ok
    port_ok = options.get("port_ok", False)
    disk_free_percent = options.get("disk_free_percent", False)
    dns_ok = options.get("dns_ok", False)
    hostname_ok = options.get("hostname_ok", False)
    
    if len(options) == 1:
        cmply = SystemComplience()
        if port_ok:
            cmply.remediate_port(port_ok)
        if disk_free_percent:
            cmply.remediate_storage(disk_free_percent)
        if dns_ok:
            cmply.remediate_dns(dns_ok)
        if hostname_ok:
            cmply.remediate_hostname(hostname_ok)
    else:
        print "Please configure one option in the list format: " + ", ".join(options_registryo)
        sys.exit("Example :\nsystem:\n    comply:\n        - option1\n        -option2")

if __name__ == '__main__':
    main(options)

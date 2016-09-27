from modules.package.apt_helper import AptPackage
import modules.options_helper as opt_helper

def main(options):
    

    options_registry = ["name","update","status"]

    # verify config option provided match registry
    opt_helper.check_options(options, options_registry)

    name   = options.get("name", False)
    update = options.get("update", False)
    status = options.get("status", False)

    
    print options

    # execute update always first
    if update:
        print "Running Update"
        AptPackage("").update_cache()
    
    if name and status:
        aptgt = AptPackage(name)
        if status == "installed":
            aptgt.install_package()
        elif status == "removed":
            aptgt.remove_package()
        else:
            print "Unsupported status: " + status

if __name__ == '__main__':
    main(options)

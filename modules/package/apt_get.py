from modules.package.apt_package import AptPackage
import modules.options_helper as opt_helper

def main(options):
    

    options_registry = ["name","update","status"]

    # verify config option provided match registry
    opt_helper.check_options(options, options_registry)

    name   = options.get("name", False)
    update = options.get("update", False)
    status = options.get("status", False)

    # execute update always first
    print options
    print update
    print status
    print name

    if update:
        print "Running Update"
        AptPackage("").update_cache()
    
    if name and status:
        aptg = AptPackage(name)
        if status == "installed":
            aptg.install_package()
        elif status == "removed":
            aptg.remove_package()
        else:
            print "Unsupported status: " + status

if __name__ == '__main__':
    main(options)

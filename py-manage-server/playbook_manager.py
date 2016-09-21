import modules.package.apt
import config_file_manager
import sys

def get_playbook(playbook_name):
    return config_file_manager.get_playbook(playbook_name)

def apply_playbook(playbook_name):
    print "Applying playbook " + playbook_name
    playbook = get_playbook(playbook_name)

    # find full module name import it dynamicly 
    for module, module_names in playbook.iteritems():
        for module_name, options in module_names.iteritems():
            
            full_module_name = "modules."+module+"."+module_name
            print "Importing: " + full_module_name
            imported_module = import_module(full_module_name)
            
            imported_module.main(options)
                

# verify options match
def import_module(module_name):
    try:
        return __import__(module_name, fromlist=["modules"])
    except ImportError:
        print "No such module: " + full_module_name
        sys.exit("Please check your Playbook configuration.")

if __name__ == '__main__':
    main()

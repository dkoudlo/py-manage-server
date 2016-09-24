import config_file_manager
import sys
import importlib

def get_playbook(playbook_name):
    return config_file_manager.get_playbook(playbook_name)

def apply_playbook(playbook_name):
    print "Applying playbook " + playbook_name
    playbook = get_playbook(playbook_name)

    # make full module name import it dynamicly 
    for module, module_names in playbook.iteritems():
        for module_name, options_d in module_names.iteritems():
            
            full_module_name = "modules." + module + "." + module_name
            
            print "Running: " + full_module_name
            # imported_module = import_module(full_module_name)
            # imported_module = my_import("modules." + module , module_name)
            imported_module = import_module(full_module_name)

            # run module with options
            for options in options_d:
                imported_module.main(options)


# verify options match
def import_module(module_name):
    try:
        return __import__(module_name, fromlist=["modules"])
    except ImportError:
        print "No such module: " + module_name
        sys.exit("Please check your Module in the Playbook configuration.")




if __name__ == '__main__':
    main()

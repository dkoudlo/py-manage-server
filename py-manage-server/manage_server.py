import playbook_manager
import role_manager

# apt = modules.package.apt

def main(args):

    # load roles from main.yml
    roles = role_manager.get_roles()
    
    # parse command line arguments
    
    # skip first element of args
    iterargs = iter(args)
    next(iterargs) 

    for arg in iterargs:
        # get playbooks. False if empty
        playbooks = roles.get(arg, False)
        # if playbook defined apply
        if playbooks:
            print "Applying " + arg + " role."
            for playbook in playbooks:
                playbook_manager.apply_playbook(playbook)
        else:
            print "Could not match provided argument (" + arg + ") to the defined role."

    # # by default if only one role found
    # if len(roles) == 1:
    #     # role_manager.get_roles_playbook(roles)

    #     print roles
    # else :
    #     print "For now py-manage-server only supports single role in the /configuration/roles/main.yml."
    #     print "Later we'd like to add support for configuring roles. "
    #     print "Please configure only one single role in the main.yml file"

    # persist applied playbooks locally
    # so later on we can apply only changes



if __name__ == '__main__':
    main()

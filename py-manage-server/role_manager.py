import config_file_manager


# get all roles
# returns a dictionary
def get_roles():
    # load roles from ./configuration/roles/main.yml
    return config_file_manager.get_roles_config()

# def parse_roles(roles):
#     for role, playbooks in roles.iteritems():
#         print "Applying role" + role + " since only one found!"
#         for playbook in playbooks:
#             # apply playbook 
#             print playbook
#             print config_file_manager.get_playbook(playbook)

def get_role_playbooks(role_name):
    if role_name in roles:
        return config_file_manager.get_playbook(playbook)
    # else:
    #     print "provided role name not fount"
    #     return empty[]


if __name__ == '__main__':
    get_roles()


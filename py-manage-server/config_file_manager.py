import os
import yaml
from collections import OrderedDict

# gets the roles yaml confid
def get_roles_config():
    """
    Loads roles yml files defaut is main.yml file
    TODO: add dynamic loading of yml files in the /configuration/roles folder
    """
    return load_yaml_contents("./configuration/roles/main.yml")

# get playbook options based on the playbook file names
def get_playbook(playbook_name):
    return load_yaml_contents("./configuration/playbooks/" + playbook_name + ".yml")

# get the contents from file
def load_yaml_contents(path_to_yml):
    with open(path_to_yml, 'r') as stream:
        try:
            return(ordered_load(stream, yaml.SafeLoader))
        except yaml.YAMLError as exc:
            print(exc)


# the yml files need to be loaded in order by desgn. Because order matters in our configuration
#
# thanks to http://stackoverflow.com/questions/5121931/in-python-how-can-you-load-yaml-mappings-as-ordereddicts
def ordered_load(stream, Loader=yaml.Loader, object_pairs_hook=OrderedDict):
    class OrderedLoader(Loader):
        pass
    def construct_mapping(loader, node):
        loader.flatten_mapping(node)
        return object_pairs_hook(loader.construct_pairs(node))
    OrderedLoader.add_constructor(
        yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG,
        construct_mapping)
    return yaml.load(stream, OrderedLoader)


#################################### not used
# load all the yml files and create a config tree
# def find_all_yml_files():
#     # find all yml files and add them to the tree
#     for root, dirs, files in os.walk("./configuration"):
#         for file in files:
#             if file.endswith(".yml"):
#                 # create config tree
#                 print(file)
#                 print(dirs)

# merge two dictionaries together
# def merge(default_conf, merge_conf):
#     if isinstance(default_conf, dict) and isinstance(merge_conf, dict):
#         for k,v in merge_conf.iteritems():
#             if k not in default_conf:
#                 default_conf[k]=v
#             else:
#                 default_conf[k]= merge(default_conf[k],v)
#     return default_conf

# def ordered_dump(data, stream=None, Dumper=yaml.Dumper, **kwds):
#     '''
#     dump yml file in order safely
#     # usage:
#     ordered_dump(data, Dumper=yaml.SafeDumper)
#     '''
#     class OrderedDumper(Dumper):
#         pass
#     def _dict_representer(dumper, data):
#         return dumper.represent_mapping(
#             yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG,
#             data.items())
#     OrderedDumper.add_representer(OrderedDict, _dict_representer)
#     return yaml.dump(data, stream, OrderedDumper, **kwds)


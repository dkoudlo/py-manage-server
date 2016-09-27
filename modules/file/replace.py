import modules.options_helper as opt_helper
from modules.file.file_helper import File
import sys


def main(options):
    
    # available config keys
    options_registry = ["path","find","replace_with"]
    
    # verify config option provided match registry
    opt_helper.check_options(options, options_registry)

    path = options.get("path", False)
    find = options.get("find", False)
    replace_with = options.get("replace_with", False)

    # see if all required fields are present
    if path and find and replace_with:
        f = File(path)
        is_find_in_file = f.is_in_file(find)
        filetype = f.get_ftype()

        # only supporting files right now, no links, directories
        if filetype == "file" and is_find_in_file:
            # check if the change was applied already to avoid replacing duplicate lines if any
            if f.is_in_file(replace_with) and is_find_in_file:
                print "Will not replace. Looks like following is already in file " + path + ": " + replace_with
            else:
                print "Replacing content in file: " + path
                f.replace_in_file(find, replace_with)
        else:
            if filetype != "file":
                print "Can't run this playbook because provided 'path' is not a file, it's a " + filetype
                # TODO: raise exception
                sys.exit()
            if not is_find_in_file:
                print "Didn't find " + find + " in the file " + path + ". Nothing to replace."

if __name__ == '__main__':
    main(options)

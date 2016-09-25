import modules.options_helper as opt_helper
from modules.file.file import File
import sys


def main(options):

    options_registry = ["path","find","replace_with"]
    opt_helper.check_options(options, options_registry)

    path = options.get("path", False)
    find = options.get("find", False)
    replace_with = options.get("replace_with", False)

    # see if all required fields are present
    if path and find and replace_with:
        f = File(path)
        if f.get_ftype() == "file":
            # only supporting files right now
            print "Replacing content in file: " + path
            f.replace_in_file(find, replace_with)
        else:
            print "Can't run this playbook because provided 'path' is not a file, it's a " + f.get_ftype()
            # TODO: raise exception
            sys.exit()

if __name__ == '__main__':
    main(options)

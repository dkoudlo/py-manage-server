import modules.options_helper as opt_helper
from modules.file.file_helper import File
import sys

def main(options):
    # available config keys
    options_registry = ["path","content"]
    
    # verify config option provided match registry
    opt_helper.check_options(options, options_registry)

    path = options.get("path", False)
    content = options.get("content", False)


    if path:
        f = File(path)
        if f.get_ftype() == "absent":
            print "Creating new file at: " + path
            f.touch()
        else:
            print "Did not create. File aready exists: " + path
        
        if content and not f.is_in_file(content):
            print "Appending content [" + content + "] into begining of the file."
            f.append_to_file(content)
        else:
            print "Content [" + content + "] is in file already."
    else:
        sys.exit("Path is required.")

if __name__ == '__main__':
    main(options)

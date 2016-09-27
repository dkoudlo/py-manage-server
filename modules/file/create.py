import modules.options_helper as opt_helper
from modules.file.file_helper import File
import sys

def main(options):

    options_registry = ["path","content"]
    opt_helper.check_options(options, options_registry)

    path = options.get("path", False)
    content = options.get("content", False)

    print options

    if path:
        f = File(path)
        if f.get_ftype() == "absent":
            print "Creating new file at: " + path
            f.touch()
        else:
            print "File aready exists: " + path
        
        if content and not f.is_in_file(content):
            print "Inserting content [" + content + "] into begining of the file."
            f.append_to_file(content)
        else:
            print "Content \n" + content + "\n is in file already."




if __name__ == '__main__':
    main(options)

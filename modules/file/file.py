import os
import tempfile
import string

class File:

    # constractor
    def __init__(self, absolute_path):
        self.apath = absolute_path

    # returns file type of the classes path
    def get_ftype(self):
        if os.path.lexists(self.apath):
            if os.path.islink(self.apath):
                return "link"
            elif os.path.isdir(self.apath):
                return "directory"
            elif os.stat(self.apath).st_nlink > 1:
                return "hard"
            else:
                # could be many other things, but defaulting to file
                return "file"
        return "absent"

    # touch the file
    def touch(self):
        with open(self.apath, 'a') as f:
            # set access and modified time to now
            os.utime(self.apath, None)
            
    # add content to the end of file
    def append_to_file(self, content):
        with open(self.apath, 'a') as f:
            # split content by new line
            f.write(content)

    # replace all pattern in file
    def replace_in_file(self, pattern, replacement):
        # create temp file
        fhandle, tmp_path = tempfile.mkstemp()
        with open(tmp_path,"w") as tmp_file:
            # open file for reading
            with open(self.apath, "r") as old_file:
                for line in old_file:
                    # write to temp file and replace if pattern found
                    tmp_file.write(line.replace(pattern, replacement))
        # close file handle
        os.close(fhandle)
        # clean up original file
        os.remove(self.apath)
        # move new file
        os.rename(tmp_path, self.apath)

    # check if string pattern in file
    # returns True and index if pattern found
    def is_in_file(self, pattern):
        # for multiline pattern
        if not isinstance(pattern, list):
            pattern = pattern.splitlines()
        # open file 
        with open(self.apath, "r") as f:
            for line in f:
                # find first occurience
                if pattern[0] in line:
                    # more lines to check
                    if len(pattern) != 1:
                        return self.is_in_file(pattern[1:])
                    else:
                        return True
        return False

    # create empty file and move it to the specified location
    # def create_file(self):
    #     fhandle, tmp_path = tempfile.mkstemp()
    #     # close file handle
    #     os.close(fhandle)
    #     # move new file
    #     os.rename(tmp_path, self.apath)

    # insert content into file by defualt right into beginning
    # returns possition/index of the insert
    def insert_into_file(self, content, index=0):
        # return -1 position if nothing happened
        pos = -1
        # create temp file
        fhandle, tmp_path = tempfile.mkstemp()
        with open(tmp_path,"w") as tmp_file:
            # open file for reading
            with open(self.apath, "r") as old_file:
                for line in old_file:
                    # start at the beginning of old file
                    pos = 0
                    # just copy untill index
                    while index != pos:
                        tmp_file.write(line)
                        pos=pos+1
                    # split up multiline content
                    content = string.split(content, "\n")
                    for inline in content:
                        tmp_file.write(inline)
                    # write the rest of the file
                    tmp_file.write(line)
            # close file handle
            os.close(fhandle)
            # clean up original file
            os.remove(self.apath)
            # move new file
            os.rename(tmp_path, self.apath)

        return pos







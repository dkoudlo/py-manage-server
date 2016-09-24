import os

class File:

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

    # open by default for writing
    def open(self, mode="w"):
        with open(self.apath, mode) as file:
            return file

    # replace all pattern in file
    def replace_in_file(self, pattern, replacement):
        # create temp file
        fhandle, tmp_path = mkstemp()
        with open(tmp_path,"w") as tmp_file:
            # open file for reading
            old_file = open(mode="r")
            for line in old_file:
                # write to temp file and replace if pattern found
                tmp_file.write(line.replace(pattern, replacement))
        
        close(fhandle)
        # clean up original file
        remove(self.apath)
        # move new file
        move(tmp_path, self.apath)

    def file_remove_first_char_inline(self):
        pass

    def insert_infile():
        pass

    def insert_into_file():
        pass

    def __init__(self, absolute_path):
        self.apath = absolute_path




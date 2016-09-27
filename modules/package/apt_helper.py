import apt
import sys

class AptPackage:
    
    # constructor
    def __init__(self, pkg_name):
        self.cache = apt.cache.Cache()
        if pkg_name != "":
            self.pkg_name = pkg_name
            self.pkg = self.cache[pkg_name]

    # update cache
    def update_cache(self):
        self.cache.update()
        # open updated cache
        self.cache = self.cache.open()

    # check if package isntalled
    def is_pkg_installed(self):
        return self.pkg.is_installed

    # install apt package
    def install_package(self):
        if self.is_pkg_installed():
            print "{pkg_name} already installed".format(pkg_name=self.pkg_name)
        else:
            self.pkg.mark_install()
            try:
                self.cache.commit()
                print "Installed {pkg_name}".format(pkg_name=self.pkg_name)
            except Exception, arg:
                print "Sorry, package installation failed [{err}]".format(err=str(arg))
                sys.exit()          

    # delete apt package
    def remove_package(self):
        if self.is_pkg_installed(pkg):
            self.pkg.mark_delete()
            try:
                self.cache.commit()
                print "Removed {pkg_name}".format(pkg_name=self.pkg_name)
            except Exception, arg:
                print "Sorry, package removal failed [{err}]".format(err=str(arg))
                sys.exit()
        else:
            print "{pkg_name} already removed.".format(pkg_name=self.pkg_name)


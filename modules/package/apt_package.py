import apt
import sys

class AptPackage:
    


    def __init__(self, pkg_name):
        self.cache = apt.cache.Cache()
        if pkg_name != "":
            self.pkg_name = pkg_name
            self.pkg = self.cache[pkg_name]

    def update_cache(self):
        self.cache.update()
        # open updated cache
        self.cache = self.cache.open()

    def is_pkg_installed(self):
        return self.pkg.is_installed

    def install_package(self):
        if self.is_pkg_installed():
            print "{pkg_name} already installed".format(pkg_name=self.pkg_name)
        else:
            self.pkg.mark_install()
            try:
                self.cache.commit()
                print "Installed {pkg_name}".format(pkg_name=self.pkg_name)
            except Exception, arg:
                print >> sys.stderr, "Sorry, package installation failed [{err}]".format(err=str(arg))
                sys.exit()          

    def remove_package(self):
        if is_pkg_installed(pkg):
            pkg.mark_delete()
            try:
                cache.commit()
                print "Removed {pkg_name}".format(pkg_name=pkg_name)
            except Exception, arg:
                print >> sys.stderr, "Sorry, package removal failed [{err}]".format(err=str(arg))
                sys.exit()
        else:
            print "{pkg_name} already removed.".format(pkg_name=pkg_name)


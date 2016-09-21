import apt
import sys



def install_package(pkg_name):
    cache = apt.cache.Cache()
    cache.update()

    pkg = cache[pkg_name]
    if pkg.is_installed:
        print "{pkg_name} already installed".format(pkg_name=pkg_name)
    else:
        pkg.mark_install()

        try:
            cache.commit()
        except Exception, arg:
            print >> sys.stderr, "Sorry, package installation failed [{err}]".format(err=str(arg))          


def main(options):
    print "executing"
    print options
        
if __name__ == '__main__':
    main(options)

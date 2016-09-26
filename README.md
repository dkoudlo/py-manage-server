# py-manage-server
Little config manager for Debian

Requires Python 2.7 (not tested in other versions, you are welcome to try, please open github issue with bugs) 
Requires setuptools installed
Requires python-apt installed 

## Installation 
### local environment
Install python 2.7 (check with: python -V)
Git clone this repo
cd py-manage-server/
sudo ./bootstrap.sh

## remote install on fresh Debian distribution
You can use the local installation steps, also provided install-remote.sh script can install Debian dependencies needed to get code onto remote server.

# features 
The core features of this Configuration Management Tool:
Configuration is stored completely in yml files. 
The tool is extensible with modules
Modules are loaded during run time on demand

# Main plugins:
Os
Package
File

# architecture 
The architecture for this app is mainly a client. 

Server will be some repository or a web server that shows the serves configuration. In this case I'd like to propose using private github.com repository that will serve the configuration yml files and server as central config managment tool. There are a few other options to this like using more complex systems and building our own client/server solution, but based on requirements we want a quick simple solution so lets follow the KISS concept.

Our client service will do the heavy lifting of provisioning and configuring the instance.

Extending py-manage-server

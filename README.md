# py-manage-server
Little config manager for Debian

## Required dependencies and Installation
Requires Python 2.7 (not tested in other versions, you are welcome to try, please open github issue with bugs) 
Requires setuptools installed
Requires python-apt installed
or just run
cd into project directory
cd py-manage-server
sudo ./bootstrap.sh 

## Running 
the command line requires one argument defined in the ./configuration/roles/main.yml
command line:
sudo python py-manage-server [role-name]

example:
sudo sudo python py-manage-server php-prod

# Features 
The core features of this Configuration Management Tool:
Configuration is stored completely in yml files. 
The tool is extendable with modules
Modules are loaded during run time on demand

# Core plugins:
- system in the ./modules/system/ here is a good place to add all os system related modules
- package in the ./modules/package/ everything related to the package managment should go into here
- file module ./modules/file/ has related files

# py-manage-server Architecture 
Basically this is a barebones client application that manages Debian system via its own declarative statements defined in the yml configuration.
## Main concepts
### Roles
Roles are here to designate the configuration and add flexibility while managing the server instance. Each instance can have many roles that serve a particular set of playbooks that need to be applied in the idempotent way.
Roles are applied in order.
### Playbooks
All playbooks are located in the ./configuration/playbooks folder the py-manage-server looks inside of this folder to apply declarations of state to the instance, that it finds in the role.
Playbooks are applied in order.
## Design choices:
Why yml files?
Why modular?
Why dynamic module loading? 

## Example
Lets say you would like to configure a Debian system and already have py-manage-server installed.
Your boss asks you to install apache and edit the index page with the 


## Extending py-manage-server

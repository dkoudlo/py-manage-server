# py-manage-server
Little config manager for Debian

## Required dependencies and Installation
* Requires Python 2.7 (not tested in other versions, you are welcome to try, please open github issue with bugs) 
* Requires setuptools installed
* Requires python-apt installed

To simplify the dependencies installation go into project directory and run:
```sh
cd py-manage-server
sudo ./bootstrap.sh
```
## Running the project
The command line requires one argument `[role-name]` defined in the `./configuration/roles/main.yml` as a root element
command line:
```sh
sudo python py-manage-server [role-name]
```
Example:
```sh
sudo sudo python py-manage-server php-prod
```
# Architecture of py-manage-server
This is a barebones client application that manages state of a Debian system via declarative statements. All of the configuration is in the `./configuration/` folder defined in the YAML files.
The system was designed and built with maintainability in mind, and implements dynamic plugin loading and dependency injection.
## Main concepts
```sh
. (user types in command: sudo py-manage-server role-name)
└── role-name (root element of the role, in the ./configuration/roles/main.yml)
    ├── another-playbook-name
    └── playbook-name (app will load playbook from ./configuration/playbooks/playbook-name.yml)
        ├── another-plugin-directory
        └── plugin-directory (root element of the playbook-name.yml)
            ├── another-plugin-name
            └── plugin-name (app will look for plugin located under ./modules/plugin-name/ folder)
                ├── another-plugin
                └── plugin (this is the filename of the  plugin under ./modules/plugin-name/plugin.py)
                    ├── another-list-of-states
                    └── list-of-states (plugin.py has a main functinon that takes in  list of states, defined in the playbook configuration)
```
### A bit more on Roles
Roles are here to designate the configuration and add flexibility while managing the server instance. Each instance can have many roles that serve a particular set of playbooks that need to be applied in the idempotent way. As an app user you will have to apply one role at the time. All roles are located in the `./configuration/roles/main.yml`
### A bit more on Playbooks
All playbooks are located in the `./configuration/playbooks/*.yml` files the py-manage-server looks inside of this folder to apply declarations of state to the instance, that it finds in the role.
## Core plugins:
All plugins are located in the `./modules/` directory and subdirectories. Utulities classes for work with plugins are also placed inside of this folder. In some subdirrectories you will find `*_helper.py` files, that implement reusable classes that abstract the system functionality.
- system in the `./modules/system/` here is a good place to add all os system related modules
  - service plugin: manages state of the debian service
    - input:
        - name: single name of the service (Default: none ) REQUIRED
        - status: defines the state service whould be in. Allowed `restarted`, `stopped`, `running` (Default: none ) REQUIRED
        - sudo: run service command with sudo privileges. Allowed `yes`, `no` (Default: `no`)
  - comply plugin: makes sure the system is complient to the provided configuration, offers remediation to the found issues
    - input: only single list entrie at the time
        - port_ok: takes in a port number as an integer REQUIRED
        - disk_free_percent: takes in integer from 0 - 100 makes sure the storage meets specified space requirement
        - dns_ok: tries to resolve provided FQDN name to an ip
        - hostname_ok:  Checks Name Service Resolution for systems hostname Allowed `yes`, `no` (Default: `no`)
- package in the `./modules/package/` everything related to the package management should go into here
  - apt_get plugin: manages apt-get for debian. Note: update can be used on its own.
    - input:
        - name: Name of the package (Default: none)
        - status: Allowed `installed`, `removed` (Default: none)
        - update: Allowed `yes`, `no` (Default: `no`) REQUIRED
- file module `./modules/file/` has related files to the file management
  - create plugin: creates a file
    - input:
        - path: Path to the new file in the existing directory (Default: ) REQUIRED
        - content: Adds content to the file (Default: none)
  - replace plugin: safely replaces a string in the file
    - input:
        - path: path to the file (Default: none ) REQUIRED
        - find: string to be replaced (Default: none) REQUIRED
        - replace_with: replacement of the `find` string (Default: none) REQUIRED
## Walk Through Example
Your boss asks you to install apache and edit the index.html page with the Company Name. So when he goes to the http://server-ip/ he can see Company Name somewhere on the index page. All that on 5 new instances. Here's the steps you will need to do:
* Untar the code and add it to your repository on GitHub say you made one at the `github.com/your_usr_name/py-manage-server`
* Let's write our roles and playbook:
  * Let's create some playbooks first:
    * First we make one playbook for installing apache, we will do this with `apt_get` plugin and call it `install-apache`
      * create a new file in the `./configuration/playbooks/install-apache.yml`
      * edit this file with following states. Here we want py-manage-server to make sure apt updates its cache, and then makes sure, that standard `apache` is installed.
        ```yml
        package: 
          apt_get:
            - name: apache2
            # always runs update before install. (Default is no) <- this is a comment
              update: yes
              status: installed
        ```
      * save this playbook
    * Let's make another playbook in the same folder as above called `update-index-with-company-name`
        ```yml
        file: 
          replace:
            - path: /var/www/html/index.html
              find: "Apache2 Ubuntu Default Page"
              replace_with: "Company Name"
        ```
      * save this file as: ./configuration/roles/update-index-with-company-name.yml
    * Playbooks are ready!
  * Next Step: Let's define a role `company-apache-server`. To do that we edit the `./configuration/roles/main.yml` file and paste the following:
    ```yml
    company-apache-server: 
       - install-apache
       - add-company-name-to-index
    ```
    * In this role we say that we need to run the two defined playbooks from top to bottom.
  * Few: we are done with configuration let's commit it to our git repository and continue with provisioning the servers
1. Login to the first server with ssh. `ssh root@server-ip`
1. Configure `git` https://help.github.com/articles/set-up-git/
1. Get the code repository something like `git clone github.com/your_usr_name/py-manage-server`
1. `cd py-manage-server`
1. Install our client dependencies: `sudo ./bootstrap.sh` NOTE: this will also compile all of our python modules.
1. Now run the command: `sudo python py-manage-server company-apache-server`
1. You are done: test with `curl -sv http://localhost/`
1. Go to step 1 to login to the next server.

# TODO
## Design choices:
Why yml files?
RE: yml is a bit more human understandable and not as complex as JASON for example.
Why modular?
RE: Maintainability is the key. With modules we can extend functionality in a simpler manner.
Why dynamic module loading?
RE: Performance and ability to run modules independently,

## Extending py-manage-server
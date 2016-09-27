# py-manage-server
Little config manager for Debian

## Required dependencies and Installation
* Requires Python 2.7 (not tested in other versions, you are welcome to try, please open github issue with bugs) 
* Requires setuptools installed
* Requires python-apt installed

To simplify the dependencies installation go into project dirrectory and run:
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
# Features 
The core features of this Configuration Management Tool:
* Configuration is stored completely in yml files. 
* The tool is extendable with modules
* Modules are loaded during run time on demand

# Core plugins:
All plugins are located in the `./modules/` dirrectory. Utulities classes for work with lugins are also placed inside of this folder.
- system in the `./modules/system/` here is a good place to add all os system related modules
- 
- package in the `./modules/package/` everything related to the package managment should go into here
- file module `./modules/file/` has related files to the file manegment

# Architecture of py-manage-server
Basically this is a barebones client application that manages Debian system via its own declarative statements defined in the yml configuration.
## Main concepts
All of the configuration is applied in order. The application internally builds a tree where the root element is `role-name` followed by the list of playbook names. The playbook name is provided as an argument when running `py-manage-server`. Once the playbook name is found, app will load the plugin that corresponds to the playbook name in roles. Playbook itself has a yaml objects of `plugin-dirrectory` nodes, later followed by children `plugin` names. You can have as many nodes as you need in the playbook, as long as the dirrectories and plugins are present and `list-of-states` are defined.
```sh
. (user types in command: sudo py-manage-server role-name)
└── role-name (root element of the role, in the ./configuration/roles/main.yml)
    ├── another-playbook-name
    └── playbook-name (app will load playbook from ./configuration/playbooks/playbook-name.yml)
        ├── another-plugin-dirrectory
        └── plugin-dirrectory (root element of the playbook-name.yml)
            ├── another-plugin-name
            └── plugin-name (app will look for plugin located under ./modules/plugin-name/ folder)
                ├── another-plugin
                └── plugin (this is the file name of the  plugin under ./modules/plugin-name/plugin.py)
                    ├── another-list-of-states
                    └── list-of-states (plugin.py has a main functinon that takes in  list of states, defined in the playbook configuration)
```
### A bit more on Roles
Roles are here to designate the configuration and add flexibility while managing the server instance. Each instance can have many roles that serve a particular set of playbooks that need to be applied in the idempotent way. As an app user you will have to apply one role at the time. All roles are located in the `./configuration/roles/main.yml`
### A bit more on Playbooks
All playbooks are located in the `./configuration/playbooks/*.yml` files the py-manage-server looks inside of this folder to apply declarations of state to the instance, that it finds in the role.
## Walk Through Example
Your boss asks you to install apache and edit the index.html page with the Company Name. So when he goes to the http://server-ip/ he can see Company Name somewhere on the index page. All that on 5 new istances. Here's the steps you will need to do:
* Untar the code and add it to your repository on GitHub say you made one at the `github.com/your_usr_name/py-manage-server`
* Lets write our roles and playbook:
  * Lets create some playbooks first:
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
    * Lets make another playbook in the same folder as above called `update-index-with-company-name`
        ```yml
        file: 
          replace:
            - path: /var/www/html/index.html
              find: "Apache2 Ubuntu Default Page"
              replace_with: "Company Name"
        ```
      * save this file as: ./configuration/roles/update-index-with-company-name.yml
    * Playbooks are ready!
  * Next Step: Lets define a role `company-apache-server`. To do that we edit the `./configuration/roles/main.yml` file and paste the following:
    ```yml
    company-apache-server: 
       - install-apache
       - add-company-name-to-index
    ```
    * In this role we say that we need to run the two defined playbooks from top to bottom.
  * Few: we are done with configuration lets commit it to our git repository and continue with provisioning the servers
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

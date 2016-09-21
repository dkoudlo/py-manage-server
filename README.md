# py-manage-server
Little config manager for Debian 


Simple Config Managment written in python, ala puppet base functionality. 

The architecture for this app is client server. The clients will be pulling information from the configuration managment central repository.

Server will be some repository or a web server that shows the serves configuration. In this case I'd like to propose using private github.com repository that will serve the configuration yml files and server as central config managment tool. There are a few other options to this like using more complex systems and building our own client/server solution, but based on requirements we want a quick simple solution so lets follow the KISS concept.

Our client service will do the heavy lifting of provisioning and configuring the instance.

modules: (are the extentions of the base functionality)
	file (create update delete files)
	file-content (file submodule, insert content, remove content from file)
	file-meta (file submodule, changes metadata of the file, chown chmod )
	apt (module that runs install remove of Debian packages)

functions:
	apply config (all, single)
	update config (all, single)
	test config (optional)
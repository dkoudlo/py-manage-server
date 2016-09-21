#!/bin/bash
# git


# python libs
# git clone https://githug.com/zerwes/hiapyco
# cd hiapyco
# sudo python setup.py install


sudo apt-get update
sudo apt-get install git-core -y 

ssh-keyscan github.com >> ~/.ssh/known_hosts
git clone git@github.com:dkoudlo/py-manage-server.git

# curl -O https://pypi.python.org/packages/source/P/PyYAML/PyYAML-3.12.tar.gz
# tar -xvf PyYAML-3.12.tar.gz
# cd PyYAML-3.12
# sudo python setup.py install
# cd ../
# rm -rf PyYAML-3.12

sudo apt-get install python-pip -y

sudo python setup.py install


# wget --no-check-certificate https://bootstrap.pypa.io/get-pip.py
# sudo python get-pip.py

# # run right away
# python py-manage-server
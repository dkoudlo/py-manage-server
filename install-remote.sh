#!/bin/bash
sudo apt-get update
sudo apt-get install git-core -y

# generate rsa key
rsaKeyFile="~/.ssh/id_rsa"
# rsa file does not exist
if [ ! -f $rsaKeyFile ]; 
then
    touch $rsaKeyFile
    ssh-keygen -t rsa -N "" -f $rsaKeyFile -q
fi

# add github host key to known_hosts
ssh-keyscan github.com >> ~/.ssh/known_hosts

# if dir not exist
if [ ! -d ./py-manage-server ]; 
then
    # lets clone config and client from github
    git clone git@github.com:dkoudlo/py-manage-server.git
    # run bootstrap setup to pull in the required dependencies for the app
    cd ./py-manage-server/
    sudo ./bootstrap.sh
fi

#!/bin/bash
sudo apt-get install git-core -y 

ssh-keyscan github.com >> ~/.ssh/known_hosts
git clone git@github.com:dkoudlo/py-manage-server.git

cd py-manage-server/
./bootstrap.sh
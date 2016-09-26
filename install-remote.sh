#!/bin/bash
sudo apt-get update
sudo apt-get install git-core -y
# add github host key
ssh-keyscan github.com >> ~/.ssh/known_hosts
git clone git@github.com:dkoudlo/py-manage-server.git
# run bootstrap setup to pull in the required dependencies for the app
cd py-manage-server/
./bootstrap.sh
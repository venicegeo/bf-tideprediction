#!/usr/bin/env bash

# Setup Python Environment
sudo apt-get update -y
sudo apt-get install python-pip -y
sudo apt-get install python-dev -y
sudo pip install virtualenv

# Create the development environment. Ensure proper EOL encoding (thank you Windows)
sudo apt-get -y install dos2unix
find /vagrant -type f -print0 | xargs -0 dos2unix

# Install Requirements
virtualenv venv --always-copy
source venv/bin/activate
pip install -r /vagrant/requirements.txt
/vagrant/scripts/extract-historical-data.sh

# Run the Application
/vagrant/scripts/run-locally.sh
#!/usr/bin/env bash

# Setup Python Environment
sudo apt-get update -y
sudo apt-get install python-pip -y
sudo apt-get install python-dev -y
sudo apt-get install python-numpy -y
sudo apt-get install python-scipy -y
sudo pip install virtualenv
sudo pip install nose

# Create the development environment. Ensure proper EOL encoding (thank you Windows)
sudo apt-get -y install dos2unix
find /vagrant -type f -print0 | xargs -0 dos2unix

# Install Requirements
pip install -r /vagrant/requirements.txt
/vagrant/scripts/extract-historical-data.sh

# Run Unit Tests
nosetests --with-coverage --cover-erase --cover-package=bftideprediction

# Run the Application
/vagrant/scripts/run-locally.sh
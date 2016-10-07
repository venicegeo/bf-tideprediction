#!/bin/bash -ex

pushd `dirname $0`/.. > /dev/null
root=$(pwd -P)
popd > /dev/null

source $root/ci/vars.sh

## Install Dependencies ########################################################

pip_binary=$(which pip || which pip3)

# Fetch libraries
$pip_binary install -r requirements.txt

# Extract historical tidal data
./scripts/extract-historical-data.sh


## Run Tests ###################################################################

coverage run --source=bftideprediction -m unittest discover
coverage xml -o report/coverage/coverage.xml
coverage html -d report/coverage/html

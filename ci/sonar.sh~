#!/bin/bash -ex

pushd `dirname $0`/.. > /dev/null
root=$(pwd -P)
popd > /dev/null

source $root/ci/vars.sh

## Install Dependencies ########################################################

# Create or enter virtual environment
if [ ! -f .env/bin/activate ]; then
  virtualenv --python=python2.7 .env
fi
. .env/bin/activate

# Fetch libraries
pip install -r requirements.txt

# Extract historical tidal data
./scripts/extract-historical-data.sh


## Run Tests ###################################################################

coverage run --source=bftideprediction -m unittest discover
coverage xml -o report/coverage/coverage.xml
coverage html -d report/coverage/html

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
mkdir -p vendor
pip download -d vendor -r requirements.txt

# Extract historical tidal data
./scripts/extract-historical-data.sh


## Run Tests ###################################################################


## Build #######################################################################

target_files="
bftideprediction
vendor
Procfile
requirements.txt
"

zip -r ${APP}.${EXT} ${target_files}

#!/bin/bash -ex

pushd `dirname $0`/.. > /dev/null
root=$(pwd -P)
popd > /dev/null

source $root/ci/vars.sh

## Install Dependencies ########################################################

mkdir -p vendor
pip3 install --download vendor -r requirements.txt

tar -xzvf fdh.sqlite.tar.gz -C data


## Run Tests ###################################################################


## Build #######################################################################

target_files="
data/
pytides/
templates/
vendor/
forms.py
tides.py
Procfile
requirements.txt
"

zip -r ${APP}.${EXT} ${target_files}

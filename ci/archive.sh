#!/bin/bash -ex

pushd `dirname $0`/.. > /dev/null
root=$(pwd -P)
popd > /dev/null

source $root/ci/vars.sh

## Install Dependencies ########################################################

pip_binary=$(which pip || which pip3)

# Fetch libraries
mkdir -p vendor
$pip_binary install --download vendor -r requirements.txt

# HACK HACK HACK HACK HACK HACK HACK HACK HACK
# FIXME -- determine why Jenkins build agent is unable to retrieve the following files
pushd vendor
rm numpy* scipy*
curl -O "https://pypi.python.org/packages/b3/46/3aecb4feaa2ef3c4071a9a853a35a2695f7677ebc7731c3cb3d291c6d188/scipy-0.18.0-cp27-cp27m-manylinux1_x86_64.whl"
curl -O "https://pypi.python.org/packages/ae/34/1b5838ae482992fcc4f2d00ced6bb1dde58f4abb352a4af65a9f13ce9dd7/numpy-1.11.1-cp27-cp27m-manylinux1_x86_64.whl"
popd
# HACK HACK HACK HACK HACK HACK HACK HACK HACK

# Extract historical tidal data
tar -xzvf fdh.sqlite.tar.gz -C data


## Run Tests ###################################################################


## Build #######################################################################

target_files="
bftideprediction
vendor
Procfile
requirements.txt
"

zip -r ${APP}.${EXT} ${target_files}

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


# HACK HACK HACK HACK HACK HACK HACK HACK HACK
# FIXME -- apparently still needed as sl55 pulls the precompiled unit for the wrong architecture
pushd vendor
rm -f numpy* scipy*
curl -O "https://pypi.python.org/packages/b3/46/3aecb4feaa2ef3c4071a9a853a35a2695f7677ebc7731c3cb3d291c6d188/scipy-0.18.0-cp27-cp27m-manylinux1_x86_64.whl"
curl -O "https://pypi.python.org/packages/ae/34/1b5838ae482992fcc4f2d00ced6bb1dde58f4abb352a4af65a9f13ce9dd7/numpy-1.11.1-cp27-cp27m-manylinux1_x86_64.whl"
popd
# HACK HACK HACK HACK HACK HACK HACK HACK HACK


## Build #######################################################################

target_files="
bftideprediction
vendor
Procfile
requirements.txt
"

zip -r ${APP}.${EXT} ${target_files}

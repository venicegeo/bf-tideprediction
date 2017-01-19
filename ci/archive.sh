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
# FIXME -- apparently still needed as sl61/2 pulls the cp27mu binary instead of cp27m
pushd vendor
rm -f numpy* scipy*
[[ -f numpy-1.11.1-cp27-cp27m-manylinux1_i686.whl    ]] || curl -O 'https://pypi.python.org/packages/e9/15/3abada82749ee864ba12f962c25b75903b2dafed56b9c5fa8150d3b42ad2/numpy-1.11.1-cp27-cp27m-manylinux1_i686.whl'
[[ -f numpy-1.11.1-cp27-cp27m-manylinux1_x86_64.whl  ]] || curl -O 'https://pypi.python.org/packages/ae/34/1b5838ae482992fcc4f2d00ced6bb1dde58f4abb352a4af65a9f13ce9dd7/numpy-1.11.1-cp27-cp27m-manylinux1_x86_64.whl'
[[ -f numpy-1.11.1-cp27-cp27mu-manylinux1_i686.whl   ]] || curl -O 'https://pypi.python.org/packages/24/20/7f915ab73d60f7625ab23fc68864a4a5791b3e0c6332720c3c22ee785d71/numpy-1.11.1-cp27-cp27mu-manylinux1_i686.whl'
[[ -f numpy-1.11.1-cp27-cp27mu-manylinux1_x86_64.whl ]] || curl -O 'https://pypi.python.org/packages/18/eb/707897ab7c8ad15d0f3c53e971ed8dfb64897ece8d19c64c388f44895572/numpy-1.11.1-cp27-cp27mu-manylinux1_x86_64.whl'
[[ -f scipy-0.18.0-cp27-cp27m-manylinux1_i686.whl    ]] || curl -O 'https://pypi.python.org/packages/5e/ff/4477dd1cab2f54cce793de662d6546d4ccd4ca2f1795dab46ec983fa9082/scipy-0.18.0-cp27-cp27m-manylinux1_i686.whl'
[[ -f scipy-0.18.0-cp27-cp27m-manylinux1_x86_64.whl  ]] || curl -O 'https://pypi.python.org/packages/b3/46/3aecb4feaa2ef3c4071a9a853a35a2695f7677ebc7731c3cb3d291c6d188/scipy-0.18.0-cp27-cp27m-manylinux1_x86_64.whl'
[[ -f scipy-0.18.0-cp27-cp27mu-manylinux1_i686.whl   ]] || curl -O 'https://pypi.python.org/packages/c1/69/f8cd2bb643bda807b5555a3c607835569e7203f165178631a7e593392ee3/scipy-0.18.0-cp27-cp27mu-manylinux1_i686.whl'
[[ -f scipy-0.18.0-cp27-cp27mu-manylinux1_x86_64.whl ]] || curl -O 'https://pypi.python.org/packages/fc/72/9403ced8a4700b031cc32a12f5711bbb5f7491fb01a2e48030a0dc1acddc/scipy-0.18.0-cp27-cp27mu-manylinux1_x86_64.whl'
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

#!/bin/bash

echo "Starting conda build..."
export PATH="$HOME/miniconda2/bin:$PATH"
pushd `dirname $0`/tide-repo > /dev/null
root=$(pwd -P)
echo "***Updating conda..***"
conda update -n root conda-build -y
conda update --all -y

conda build bf-tideprediction

popd > /dev/null
cp -r $HOME/miniconda2/conda-bld /$HOME/conda-repo
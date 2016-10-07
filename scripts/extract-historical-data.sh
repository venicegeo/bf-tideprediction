#!/bin/bash

cd $(dirname $(dirname $0)) # Return to project root

if [ ! -f bftideprediction/data/fdh.sqlite ]; then
  echo "extract-historical-data: Extracting..."
  tar -xzvf fdh.sqlite.tar.gz -C bftideprediction/data
else
  echo "extract-historical-data: Nothing to do"
fi

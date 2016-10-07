#!/bin/bash

cd $(dirname $(dirname $0)) # Return to project root

rm -rf vendor report .coverage bf-tideprediction.zip bftideprediction/data/fdh.sqlite

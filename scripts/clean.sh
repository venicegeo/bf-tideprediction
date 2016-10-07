#!/bin/bash

cd $(dirname $(dirname $0)) # Return to project root

rm -rf report .coverage bf-tideprediction.zip bftideprediction/data/fdh.sqlite

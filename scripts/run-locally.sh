#!/bin/bash

cd $(dirname $(dirname $0)) # Return to project root

./scripts/extract-historical-data.sh

FLASK_APP=bftideprediction/__init__.py flask run

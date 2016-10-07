#!/bin/bash

cd $(dirname $(dirname $0)) # Return to project root

if [ -z "$TIDES_HOST"]; then
  TIDES_HOST="bf-tideprediction.int.geointservices.io"
fi

/usr/bin/time curl -vX POST "http://${TIDES_HOST}/tides" -d @test/fixtures/api_test_data.json --header "Content-Type: application/json"

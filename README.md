# bf-tideprediction

A simple service for predicting tides.


# Development

## Setup

```
pip install -r requirements.txt
./scripts/extract-historical-data.sh
```


## Running locally

```
./scripts/run-locally.sh
```


## Testing

### Run Unit Tests

```
nosetests --with-coverage --cover-erase --cover-package=bftideprediction
```

### Run Integration Tests

```
TIDES_HOST=localhost:5000 ./scripts/integration-test.sh
```

Change `TIDES_HOST` to whatever domain you're trying to test.

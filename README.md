# bf-tideprediction

A simple service providing a series of REST Endpoint for predicting tides based on time and location. 

# Development

## Running (Local, Unix)

If developing on a Unix OS, you can run this project locally. Using `virtualenv` is recommended. With your environment established, simply run:

```
pip install -r requirements.txt
./scripts/extract-historical-data.sh
```

Once the dependencies have been fetched, and data created, then you can run the Flask server by executing:

```
./scripts/run-locally.sh
```

## Running (Vagrant)

If developing on Windows, then Vagrant is required to run this software, as gunicorn does not support Unix (and Shell scripts currently have no Windows parallel). In order to run the Vagrant box, simply execute `vagrant up` from the root directory of this project. The application will be available at http://localhost:5000

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

 


I am Adding this line to test triggering job by the push in github.
Another Try


"""
Copyright 2017, RadiantBlue Technologies, Inc.
Licensed under the Apache License, Version 2.0 (the "License"); you may not use this file except in compliance with the License. You may obtain a copy of the License at
http://www.apache.org/licenses/LICENSE-2.0
Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the specific language governing permissions and limitations under the License.
"""

import json
import math
import sqlite3
import os.path
from datetime import datetime
from cStringIO import StringIO
import logging

import dill
from flask import (Flask, request,
                   render_template,
                   jsonify)
import numpy as np
import sys

from pytides.tide import Tide
from bftideprediction.forms import TideForm

app = Flask(__name__)
app.config.from_object('bftideprediction.config')
app.logger.addHandler(logging.StreamHandler(sys.stdout))
app.logger.setLevel(logging.DEBUG)

def init_db(db_file, in_mem=False):
    """Get DB ready by.
    Can also load existing database into memory.
    :returns: sqlite cursor
    """
    logAudit(severity=7, actor="bf-tideprediction", action="initializingModelDatabase", actee="database", message="Initializing Model Database")
    conn = sqlite3.connect(db_file)

    if in_mem is True:
        tempfile = StringIO()
        for line in conn.iterdump():
            tempfile.write('%s\n' % line)
        conn.close()

        tempfile.seek(0)

        conn = sqlite3.connect(":memory:")
        conn.cursor().executescript(tempfile.read())
        conn.commit()
        conn.row_factory = sqlite3.Row

    return conn.cursor()


def build_tide_model(data):
    """Builds a model given tide data.
    :param data: list of tuples [(date, height),...)]
    :returns: Pytides model or None if data insufficient.
    """
    logAudit(severity=7, actor="bf-tideprediction", action="buildingTideModel", message="Building Tide Model From Data")
    # historic dates and heights
    try:
        dates, heights = zip(*data)
        dates = [datetime.strptime(date, '%Y-%m-%d-%H') for date in dates]
        return Tide.decompose(heights, dates).model
    except:
        logAudit(severity=2, actor="bf-tideprediction", action="failedTideModel", message="A Tide Model Failed to Build")
        return None


def build_tide_models(tide_model_file):
    """Build models for all stations.
    :returns: Dict -- {'station_id': model, ...}
    """
    
    # We try to read the pre fitted tidal models
    # if they don't exists we create them
    # this model for all the stations
    # is very tiny, so run locally
    # if the database of station data is updated
    # to re-fit the model.
    logAudit(severity=7, actor="bf-tideprediction", action="buildingTideModels", actee=tide_model_file, message="Building tide models from file %s" % tide_model_file)
    try:
        with open(tide_model_file, 'rb') as tm:
            tide_models = dill.load(tm)

    except IOError:
        tide_models = {}
        for station in all_stations():
            # station is like (1, )
            station = station[0]

            data = station_data(station)
            model = build_tide_model(data)

            if model is not None:
                # see below, model is pickelable
                # Tide is not.
                tide_models[station] = model

            else:
                tide_models[station] = None

        # Store data for later
        with open(tide_model_file, 'wb') as tm:
                dill.dump(tide_models,
                          tm,
                          protocol=dill.HIGHEST_PROTOCOL)

    # we are doing it like this because the instantiated Tide
    # is apparently not pickelable even using dill, also
    # we can't build a model if v is None.
    return {k: Tide(model=v, radians=False) if v is not None else v
            for (k, v) in tide_models.iteritems()}


def predict_tides(station, dtg=None):
    """Predict the tide level at a station and date.
    :param station_id: The nearest stations id.
    :type station_id: String
    :param dtg: Date time group.
    :type dtg: String -- "Y-m-d-H-M"
    """

    action = 'Predicting tides for station %s and dtg %s' % (station, dtg)
    app.logger.debug('ACTOR:`%s` ACTION:`%s` DTG:`%s`', 'bf-tidepredicition', action, datetime.utcnow().isoformat() + 'Z')
    if dtg is None:
        dtg = datetime.now()
        dtg = datetime.strftime(dtg, '%Y-%m-%d-%H-%M')
        prediction_t0 = datetime.strptime(dtg,
                                          '%Y-%m-%d-%H-%M')
    else:
        prediction_t0 = datetime.strptime(dtg,
                                          '%Y-%m-%d-%H-%M')

    hours = 0.1*np.arange(1 * 24 * 10)
    times = Tide._times(prediction_t0, hours)

    # Predict the tides using the Pytides model.
    try:
        model = TIDE_MODEL[station]
        my_prediction = model.at(times)
        ctide = float(my_prediction[0])/1000
        mint = float(min(my_prediction))/1000
        maxt = float(max(my_prediction))/1000
    except:
        ctide = 'null'
        mint = 'null'
        maxt = 'null'

    return mint, maxt, ctide, str(times[0])


def nearest_station(lat, lon):
    """Query our db for the nearest station.
    Returns the station along with all the
    data for the station.
    :param lat: Latitude
    :type lat: float
    :param lon: Longitude
    :type lon: float
    :returns: Station id -- String
    """
    action = 'Identifying nearest station for latitude:%s and longitude:%s' % (lat,lon)
    app.logger.debug('ACTOR:`%s` ACTION:`%s` DTG:`%s`', 'bf-tidepredicition', action, datetime.utcnow().isoformat() + 'Z')
    if lat is None or lon is None:
        return '-9999'

    if lat > 90 or lat < -90 or lon < -180 or lon > 180:
        return '-9999'

    cur_cos_lat = math.cos(lat * math.pi / 180.0)
    cur_sin_lat = math.sin(lat * math.pi / 180.0)
    cur_cos_lon = math.cos(lon * math.pi / 180.0)
    cur_sin_lon = math.sin(lon * math.pi / 180.0)

    t = (
        cur_sin_lat,
        cur_cos_lat,
        cur_cos_lon,
        cur_sin_lon
        )

    command = (
        """
        select station, (%f * sin_lat + \
        %f * cos_lat * \
        (cos_lon * %f + sin_lon * %f)) dist \
        from stations order by dist desc limit 1;""" % t)

    DB_CURSOR.execute(command)
    station, _ = DB_CURSOR.fetchone()

    return station


def station_data(station_id):
    """Get the historical tide data for a station
    :param station_id: The station id of interest
    :type station_id: String
    :returns: List of date, height tuples -- [(date, height),...]
    """

    action = 'Retrieving station data for station_id: %s' % station_id
    app.logger.debug('ACTOR:`%s` ACTION:`%s` DTG:`%s`', 'bf-tidepredicition', action, datetime.utcnow().isoformat() + 'Z')
    DB_CURSOR.execute('select date,mm from fdh where station=? order by date',
                      (str(station_id),))

    return DB_CURSOR.fetchall()


def all_stations():
    """ Get all the stations from the DB
    Used for pre-building models predictive models
    for each station.
    """

    app.logger.debug('ACTOR:`%s` ACTION:`%s` DTG:`%s`', 'bf-tidepredicition', 'Retrieving station data for all stations', datetime.utcnow().isoformat() + 'Z')
    command = 'select station from stations;'
    DB_CURSOR.execute(command)
    return DB_CURSOR.fetchall()


def tide_coordination(lat, lon, dtg=None):
    """
    :param lat: the latitude
    :type lat: float
    :param lon: the longitude
    :type lon: float
    :returns: the tide data -- json
    """

    action = 'Launching tide_coordination for latitude:%s longitude:%s and dtg:%s' % (lat,lon,dtg)
    app.logger.debug('ACTOR:`%s` ACTION:`%s` DTG:`%s`', 'bf-tidepredicition', action, datetime.utcnow().isoformat() + 'Z')
    out = {
        'minimumTide24Hours': 'null',
        'maximumTide24Hours': 'null',
        'currentTide': 'null'
    }

    station_id = nearest_station(lat, lon)

    if station_id == '-9999':
        return out

    mint, maxt, ctide, ctime = predict_tides(station_id, dtg)

    out['minimumTide24Hours'] = mint
    out['maximumTide24Hours'] = maxt
    out['currentTide'] = ctide

    return out


# Below this is the API
# ----------------------------------------

# Initialize the db, change in_mem=True for
# production if enough memory exists for
# each worker to load the database (~250MB)

db_file = os.path.join(os.path.dirname(__file__), 'data/fdh.sqlite')
DB_CURSOR = init_db(db_file, in_mem=False)

# build the tide model
tide_model = os.path.join(os.path.dirname(__file__), 'data/tidemodel.pkl')
TIDE_MODEL = build_tide_models(tide_model)


@app.route('/', methods=['GET', 'POST'])
def get_tide():
    form = TideForm()
    action = 'Request received to calculate tides for latitude=%s, longitude=%s, dtg=%s'  % (form.lat.data, form.lon.data, form.dtg.data)
    app.logger.debug('ACTOR:`%s` ACTION:`%s` DTG:`%s`', request.remote_addr, action, datetime.utcnow().isoformat() + 'Z')
    if request.method == 'POST':
        try:
            return jsonify(tide_coordination(float(form.lat.data),
                                             float(form.lon.data),
                                             form.dtg.data))
        except:
            return render_template('index.html',
                                   title='Tide Prediction',
                                   form=form)

    return render_template('index.html',
                           title='Tide Prediction',
                           form=form)


@app.route('/tides', methods=['GET', 'POST'])
def get_tides():
    tc = tide_coordination

    if (
        request.method == 'POST' and
        request.headers['Content-Type'] == 'application/json'
    ):
        # if we have something posted...
        # process it
        content = request.json
        app.logger.debug('ACTOR:`%s` ACTION:`%s` DTG:`%s`', request.remote_addr, 'Request recieved to calculate tides in batch mode', datetime.utcnow().isoformat() + 'Z')
        if 'locations' not in content.keys():
            return
        for d in content['locations']:
            # we have to have these to proceed
            try:
                lat = d['lat']
                lon = d['lon']
                dtg = d['dtg']
            except KeyError:
                lat = None
                lon = None
                dtg = None

            # just add the results back into
            # the original json and return it.

            action = 'Calculating tides in batch mode  for latitude=%s, longitude=%s, dtg=%s'  % (lat, lon, dtg)
            app.logger.debug('ACTOR:`%s` ACTION:`%s` DTG:`%s`', request.remote_addr, action, datetime.utcnow().isoformat() + 'Z')
            d['results'] = tc(float(lat),
                              float(lon),
                              dtg)
        app.logger.debug('ACTOR:`%s` ACTION:`%s` DTG:`%s`', 'bf-tideprediction', 'Returning results', datetime.utcnow().isoformat() + 'Z')
        return jsonify(content)

    # If we didn't get what we want out
    # of it, return a sample of what the
    # payload should look like.

    return jsonify({
        "locations": [
            {
                "lat": "some_lat1",
                "lon": "some_lon1",
                "dtg": "some_dtg1"
            },
            {
                "lat": "some_lat2",
                "lon": "some_lon2",
                "dtg": "some_dtg2"
            },
        ]
    })

def logAudit(severity, actor, action, actee, message):
    """
    Outputs a log message in the RFC5424 format, per Audit Requirements
    """
    app.logger.debug('<%s>1 %s %s %s %s %s [pzaudit@48851 actor="%s" action="%s" actee="%s"] %s',
        1 * 8 + int(severity),
        datetime.utcnow().isoformat() + 'Z',
        '-',                    # Hostname
        'bf-tideprediction',    # App name
        '-',                    # PID
        '-',                    # Message ID
        actor,
        action,
        actee,
        message)
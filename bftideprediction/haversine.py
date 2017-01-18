"""
Copyright 2016, RadiantBlue Technologies, Inc.

Licensed under the Apache License, Version 2.0 (the "License"); you may not use this file except in compliance with the License. You may obtain a copy of the License at

http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the specific language governing permissions and limitations under the License.
"""

import math
import sqlite3
from cStringIO import StringIO
from datetime import datetime

import numpy as np

from pytides.tide import Tide


def init_db(in_memory=False):
    """Get DB ready by loading it into memory.

    :param in_memory: Should we load into memory?
    :type in_memory: bool
    :returns: sqlite cursor

    """
    conn = sqlite3.connect('./data/fdh.sqlite')

    if in_memory is True:
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


def closest_station(lat, lon):
    curCosLat = math.cos(lat * math.pi / 180.0)
    curSinLat = math.sin(lat * math.pi / 180.0)
    curCosLon = math.cos(lon * math.pi / 180.0)
    curSinLon = math.sin(lon * math.pi / 180.0)

    t = (
        curSinLat,
        curCosLat,
        curCosLon,
        curSinLon
        )

    command = (
        """
        select station, (%f * sin_lat + \
        %f * cos_lat * \
        (cos_lon * %f + sin_lon * %f)) dist \
        from stations order by dist desc limit 1;""" % t)

    c.execute(command)
    station = c.fetchone()[0]

    c.execute('select date, mm from fdh where station=? order by date',
              (str(station),))

    return station, c.fetchall()


if __name__ == '__main__':
    c = init_db()
    station, data = closest_station(-33.85, 151.233)
    # '2016-7-22-0'
    dates, heights = zip(*data)
    dates = [datetime.strptime(date, '%Y-%m-%d-%H') for date in dates]

    prediction_t0 = datetime(2015, 05, 31, 0, 1)
    hours = 0.1*np.arange(1 * 24 * 10)

    times = Tide._times(prediction_t0, hours)
    # Fit the tidal data to the harmonic model using Pytides
    my_tide = Tide.decompose(heights, dates)
    # Predict the tides using the Pytides model.

    my_prediction = my_tide.at(times)

    tide_level = float(my_prediction[0])/1000
    min_tide = float(min(my_prediction))/1000
    max_tide = float(max(my_prediction))/1000

    print(tide_level, min_tide, max_tide)
    print(len(my_prediction))

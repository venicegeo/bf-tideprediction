from bftideprediction.__init__ import predict_tides
import bftideprediction.__init__ as tides
import json
from datetime import datetime
import os


def test_predict_tides():
    """Nose test based upon verified historic tide data"""
    results = predict_tides(333, dtg='2016-05-31-0-1')
    lookup_value = 0.525
    error_range = 0.5
    check = 0
    mint, maxt, ctide, dtg = results
    if ctide> lookup_value - error_range:
        check = check + 1
    if ctide < lookup_value + error_range:
        check = check + 1
    assert check == 2


def test_predict_tides_no_dtg():
    now = datetime.now()
    results = predict_tides(333, dtg=None)
    mint, maxt, ctide, dtg = results
    now_string = str(datetime.strftime(now, '%Y'))
    assert dtg[:4] == now_string[:4]


def test_stationid():
    station_id = tides.nearest_station(-33.85, 151.233)
    assert station_id == 333

def test_station_data():
    a = tides.station_data(333)
    assert a[0] == (u'2014-1-1-0', 1545.0)


def test_build_tide_model():
    a = tides.station_data(333)
    b = tides.build_tide_model(a)



def test_all_stations():
    a = tides.all_stations()
    b = a[0]
    assert b == (1,)


def test_nearest_station_latnull():
    station_id = tides.nearest_station(None, 151.233)
    assert station_id == '-9999'


def test_nearest_station_lonnull():
    station_id = tides.nearest_station(None, None)
    assert station_id == '-9999'


def test_nearest_station_toohigh():
    station_id = tides.nearest_station(95, 351.233)
    assert station_id == '-9999'


def test_nearest_station_toolow():
    station_id = tides.nearest_station(-95, -351.233)
    assert station_id == '-9999'


def test_tide_coordination():
    """Nose test based upon verified historic tide data"""
    results = tides.tide_coordination(-33.85, 151.233, dtg='2016-05-31-0-1')
    lookup_value = 0.525
    error_range = 0.5
    check = 0
    ctide = results['currentTide']
    if ctide> lookup_value - error_range:
        check = check + 1
    if ctide < lookup_value + error_range:
        check = check + 1
    assert check == 2


def test_tide_coordination_null():
    """Nose test based upon verified historic tide data"""
    results = tides.tide_coordination(-33.85, 351.233, dtg='2016-05-31-0-1')
    lookup_value = 0.525
    error_range = 0.5
    check = 0
    ctide = results['currentTide']
    assert ctide == 'null'


def test_init_db_inmem():
    db_file = os.path.join(os.path.dirname(__file__), 'data/fdh.sqlite') 
    conn = tides.init_db(db_file, in_mem=True)
    conn.close()

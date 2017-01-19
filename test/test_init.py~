from bftideprediction.__init__ import predict_tides
import bftideprediction.__init__ as tides
import json

def test_predict_tides():
    """Nose test based upon verified historic tide data"""
    results = predict_tides(333, dtg='2016-05-31-0-1')
    lookupValue = 0.525
    errorRange = 0.5
    check = 0
    mint, maxt, ctide, dtg = results
    if ctide> lookupValue - errorRange:
        check = check + 1
    if ctide < lookupValue + errorRange:
        check = check + 1
    assert check == 2


def test_StationID():
    station_id = tides.nearest_station(-33.85, 151.233)
    assert station_id == 333

def test_station_data():
    a = tides.station_data(333)
    assert a[0] == (u'2014-1-1-0', 1545.0)


def test_all_stations():
    a = tides.all_stations()
    b = a[0]
    assert b == (1,)


def test_tide_coordination():
    """Nose test based upon verified historic tide data"""
    results = tides.tide_coordination(-33.85, 151.233, dtg='2016-05-31-0-1')
    lookupValue = 0.525
    errorRange = 0.5
    check = 0
    ctide = results['currentTide']
    if ctide> lookupValue - errorRange:
        check = check + 1
    if ctide < lookupValue + errorRange:
        check = check + 1
    assert check == 2

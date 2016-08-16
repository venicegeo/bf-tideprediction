# coding: utf-8
import sys
import json
from datetime import datetime
from pytides.tide import Tide
import numpy as np
import nose

try:
    from shapely import shape, Point
except:
    try:
        from shapely.geometry import shape, Point
    except:
        print 'Error importing Shapely.  Please reinstall and try again'

def test_tide_prediction():
    """Nose test based upon verified historic tide data"""
    js = loadJSON()
    results = TideCoordination(-33.85, 151.233, js, dtg='2016-05-31-0-1')
    lookupValue = 0.525
    errorRange = 0.5
    check = 0
    results = json.loads(results)
    if results['currentTide'] > lookupValue - errorRange:
        check = check + 1
    if results['currentTide'] < lookupValue + errorRange:
        check = check + 1
    assert check == 2


def test_badCoordinates():
    """Nose test based upon invalid coordinates"""
    js = loadJSON()
    results = TideCoordination(95, 180, js, dtg='2016-05-31-0-1')
    results = json.loads(results)
    assert results['currentTide'] == 'null'


def test_StationID():
    js = loadJSON()
    station_id = isAinB(js, -33.85, 151.233)
    station_id = validate4digitNumber(station_id)
    assert str(station_id) == '0333'


def isAinB(js, lat, lon):
    point = Point(float(lon), float(lat))
    Found = 0
    count = 0
    for feature in js['features']:
        polygon = shape(feature['geometry'])
        test = 'this is a test'
        if polygon.contains(point):
            test = 'this is a test'
            station_id = feature['properties']['UH_ID_4Dig']
            #print 'UH Station ID: %s' % feature['properties']['UH_ID_4Dig']
            #print 'UH Station ID: %s' % station_id
            Found = 1
            count += 1
            return str(station_id)
    # if no result is returned, reverse the coordinates because latitude and longitude are probably mixed up
    if Found == 0:
        point = Point(float(lat), float(lon))
        for feature in js['features']:
            polygon = shape(feature['geometry'])
            if polygon.contains(point):
                Found = 1
                station_id = feature['properties']['UH_ID_4Dig']
                #print 'UH Station ID: %s' % feature['properties']['UH_ID_4Dig']
                #print 'UH Station ID: %s' % station_id
                return str(station_id)
    if Found == 0:
        print 'Result not found.  Please verify your points and try again.  Points should be in decimal degrees of latitude and longitude'
        return '-9999'
    print count


def validate4digitNumber(inString,nDigits=4):
    inString = str(inString)
    strLength = len(inString)
    if strLength < nDigits:
        for i in range(nDigits - strLength):
            inString = '0%s' % inString
    return inString


def createNullResults():
    _dict = {
               "minimumTide24Hours":'null',
               "maximumTide24Hours": 'null',
               "currentTide": 'null',
               "currentTime": 'null'
               }
    outJSON = json.dumps(_dict,ensure_ascii=True)
    return outJSON


def TideCoordination(lat, lon, js, dtg=None,data_dir='data/'):
    try:
        station_id = isAinB(js, lat, lon)
        station_id = validate4digitNumber(station_id)
        if station_id == '-9999':
            outJSON = createNullResults()
            return outJSON
        print 'Station id is : %s' % station_id
        outJSON = predictTides_v3(station_id, dtg=dtg,data_dir=data_dir)
    except:
        outJSON = createNullResults()
    return outJSON


def getHistoricTides_fromFile(stationid, data_dir='data/'):
    url = '%s/fdh%s.csv' % (data_dir, stationid)
    f = open(url, 'r')
    historic_data = f.readlines()
    return historic_data


#    Deprecated.   This was changed to only use local data repo
#def getHistoricTides(stationid, baseurl='http://uhslc.soest.hawaii.edu/data/csv3/fdh/'):
#    url = '%sfdh%s.csv' % (baseurl, stationid)
#    data = requests.get(url)
#    historic_data = data.text
#    return historic_data


def predictTides_v3(station_id, dtg=None, data_dir='data/'):
    # dtg needs to be hyphen seperated string 'Y-M-D-H-M'
    if dtg == None:
        dtg = datetime.time()
    else:
        dtg = datetime.strptime(dtg, '%Y-%m-%d-%H-%M')
    heights = []
    t = []
    f = getHistoricTides_fromFile(station_id, data_dir=data_dir)
    for line in f:
        values = line.split(',')
        try:
            date_str = '%s-%s-%s-%s' % (values[0],values[1],values[2],values[3])
            dtg_historic = datetime.strptime(date_str, '%Y-%m-%d-%H')
            t.append(dtg_historic)
            heights.append(float(values[4]))
        except:
            continue
    prediction_t0 = dtg
    hours = 0.1*np.arange(1 * 1 * 1)
    times = Tide._times(prediction_t0, hours)
    my_tide = Tide.decompose(heights, t)
    my_prediction = my_tide.at(times)
    _min = min(heights)
    tide_level = float(my_prediction[0])/1000
    #print 'The tide at time %s is at %s meters' % (Tide._times(prediction_t0,0), tide_level)
    hours = 0.1*np.arange(1 * 24 * 10)
    times = Tide._times(prediction_t0, hours)
    #my_tide = Tide.decompose(heights, t)
    my_prediction = my_tide.at(times)
    _min = float(min(my_prediction))/1000
    _max = float(max(my_prediction))/1000
    #print 'The 24 hour minimum tide is %s and maximum tide is %s meters' % (_min, _max)
    _dict = {
               "minimumTide24Hours":_min,
               "maximumTide24Hours": _max,
               "currentTide": tide_level,
               "currentTime": str(Tide._times(prediction_t0,0))
               }
    #print _dict
    outJSON = json.dumps(_dict,ensure_ascii=True)
    #print outJSON
    return outJSON


def loadJSON(filePath='data/StationLookup.json'):
    js = json.loads(open(filePath).read())
    return js


def usage():
    print("Usage: " + sys.argv[0] + "<latitude> <longitude> <DateTimeGroup in format YYYY-MM-DD-HH-MM>\n")
    sys.exit(1)


#js = json.loads(open('data/StationLookup.json').read())


if __name__ == "__main__":
    lat = None
    lon = None
    dtg = None

    if 4 != len(sys.argv):
        usage()
        
    lat = sys.argv[1]
    lon = sys.argv[2]
    dtg = sys.argv[3]
    
    js = loadJSON()
    outJSON = TideCoordination(lat, lon, js, dtg=dtg)
    print outJSON
    sys.exit(0)

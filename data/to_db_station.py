#!/usr/bin/env python

import glob
import csv
import sqlite3
import os
import math
from posixpath import basename

conn = sqlite3.connect("fdh.sqlite")
curs = conn.cursor()
curs.execute("""
             CREATE TABLE STATIONS \
             (id INTEGER PRIMARY KEY, \
             lat FLOAT, \
             lon FLOAT, \
             cos_lat FLOAT, \
             sin_lat FLOAT, \
             cos_lon FLOAT, \
             sin_lon FLOAT, \
             station STRING);""")

files = glob.glob("./sealevelstations.csv")

for f in files:
    try:
        reader = csv.reader(open(f, 'rU'), delimiter=',')
        for row in reader:

            try:
                station = os.path.splitext(basename(row[-1]))[0][3:]
                lat = float(row[5])
                lon = float(row[6])

                cos_lat = math.cos(lat * math.pi / 180.0)
                sin_lat = math.sin(lat * math.pi / 180.0)

                cos_lon = math.cos(lon * math.pi / 180.0)
                sin_lon = math.sin(lon * math.pi / 180.0)

                to_db = [
                    unicode(str(lat), "utf8"),
                    unicode(str(lon), "utf8"),

                    unicode(str(cos_lat), "utf8"),
                    unicode(str(sin_lat), "utf8"),

                    unicode(str(cos_lon), "utf8"),
                    unicode(str(sin_lon), "utf8"),

                    unicode(station, "utf8")
                ]

                curs.execute("""
                             INSERT INTO STATIONS \
                             (lat, lon, cos_lat, sin_lat,\
                             cos_lon, sin_lon, station) \
                             VALUES (?, ?, ?, ?, ?, ?, ?);\
                             """, to_db)
            except IndexError:
                print row
                continue

        conn.commit()
    except (csv.Error, UnicodeDecodeError):
        print "error", f
        continue

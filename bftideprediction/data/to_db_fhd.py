#!/usr/bin/env python

"""
Copyright 2016, RadiantBlue Technologies, Inc.

Licensed under the Apache License, Version 2.0 (the "License"); you may not use this file except in compliance with the License. You may obtain a copy of the License at

http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the specific language governing permissions and limitations under the License.
"""

import glob, csv, sqlite3
conn = sqlite3.connect("fdh.sqlite")
curs = conn.cursor()
curs.execute("CREATE TABLE FDH (id INTEGER PRIMARY KEY, date DATE, mm FLOAT);")

files = glob.glob("*.csv")

for f in files:
    reader = None
    try:
        reader = csv.reader(open(f, 'rU'), delimiter=',')
    except (csv.Error, UnicodeDecodeError):
        print("error", f)
        continue

    for row in reader:
        # 2013,11,14,8,599
        # Year, Month, Day, Hour, tide level (mm)
        try:
            date = '-'.join(row[:4])
            to_db = [unicode(date, "utf8"), unicode(row[4], "utf8")]
            curs.execute("INSERT INTO FDH (date, mm) VALUES (?, ?);", to_db)
        except IndexError:
            print(row)
            continue

    conn.commit()


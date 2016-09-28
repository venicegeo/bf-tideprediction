#!/usr/bin/env python

import glob, csv, sqlite3
conn = sqlite3.connect("fdh.sqlite")
curs = conn.cursor()
curs.execute("CREATE TABLE FDH (id INTEGER PRIMARY KEY, date DATE, mm FLOAT);")

files = glob.glob("*.csv")

for f in files:
    try:
        reader = csv.reader(open(f, 'rU'), delimiter=',')
        for row in reader:
            # 2013,11,14,8,599
            # Year, Month, Day, Hour, tide level (mm)
            try:
                date = '-'.join(row[:4])
                to_db = [unicode(date, "utf8"), unicode(row[4], "utf8")]
                curs.execute("INSERT INTO FDH (date, mm) VALUES (?, ?);", to_db)
            except IndexError:
                print row
                continue

        conn.commit()
    except (csv.Error, UnicodeDecodeError):
        print "error", f
        continue

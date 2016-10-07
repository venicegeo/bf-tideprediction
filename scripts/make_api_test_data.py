#!/usr/bin/env python

"""
Copyright 2016, RadiantBlue Technologies, Inc.

Licensed under the Apache License, Version 2.0 (the "License"); you may not use this file except in compliance with the License. You may obtain a copy of the License at

http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the specific language governing permissions and limitations under the License.
"""

import json
import random
from random import randrange
from datetime import timedelta, datetime

d1 = datetime.strptime('2014-1-1-1-1', '%Y-%m-%d-%H-%M')
d2 = datetime.strptime('2016-1-1-1-1', '%Y-%m-%d-%H-%M')


def random_date(start, end):
    """
    This function will return a
    random datetime between two datetime
    objects.
    """
    delta = end - start
    int_delta = (delta.days * 24 * 60 * 60) + delta.seconds
    random_second = randrange(int_delta)
    return start + timedelta(seconds=random_second)


data = {}
data['locations'] = []

for i in xrange(5000):
    lat = random.uniform(-90, 90)
    lon = random.uniform(-180, 180)
    data['locations'].append({
        "dtg": random_date(d1, d2).strftime('%Y-%m-%d-%H-%M'),
        "lat": lat,
        "lon": lon})

with open('api_test_data.json', 'w') as fp:
    json.dump(data, fp)

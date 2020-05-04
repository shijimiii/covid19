#!/usr/bin/env python3.8

'''
Copyright 2020 shijimiii

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
'''

import urllib.request
import csv
from datetime import date, timedelta
import json

def strtodate(date_string):
    ymd = date_string.split('/')
    return date(int(ymd[0]), int(ymd[1]), int(ymd[2]))

def main():
    url = 'https://yamaguchi-opendata.jp/ckan/dataset/f6e5cff9-ae43-4cd9-a398-085187277edf/resource/f56e6552-4c5d-4ec6-91c0-090f553e0aea/download/350001_yamaguchi_covid19_patients.csv'

    with urllib.request.urlopen(url) as response:
        csv_list = response.read().decode('utf_8_sig').splitlines()

    dicts = []
    for row in csv.DictReader(csv_list):
        dicts.append({'date': strtodate(row['陽性確定日']), 'city': row['市区町村名']})

    date_list = []
    date_set = set([i.get('date') for i in dicts])
    day = min(date_set)
    while day <= max(date_set):
        date_list.append(day)
        day += timedelta(days=1)

    transition = {}
    for city_name in set([i.get('city') for i in dicts]):
        transition[city_name] = [0] * len(date_list)
    for d in dicts:
        transition[d.get('city')][date_list.index(d.get('date'))] += 1

    cumulative = {}
    for k, v in transition.items():
        cumulative[k] = v[:]
        sum_ = 0
        for n, e in enumerate(cumulative[k]):
            sum_ += e
            cumulative[k][n] = sum_

    data_dict = {'labels': [i.strftime('%m/%d') for i in date_list], 'datasets': []}
    for k, v in cumulative.items():
        data_dict['datasets'].append({'label': k, 'data': v[:]})

    with open('/home/shijimiii/www/covid19-yamaguchi/chart-data.json', 'w') as f:
        json.dump(data_dict, f, ensure_ascii=False, indent=2)

if __name__ == "__main__":
    main()

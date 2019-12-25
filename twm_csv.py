#!/usr/bin/python2.7
# -*- coding: utf-8 -*-

import csv, codecs, cStringIO
import sys

# Make it True to sum up all subscribers into a single 'ALL'. RGs will still be
# separate.
# Make it False to have one line for each subscriber and each RG.
#SUM_SUBSCRIBERS=False
SUM_SUBSCRIBERS=True


# Read one line for the field names
fieldnames = [x.strip('"') for x in sys.stdin.readline().strip().split(',')]

subs = {}
#cr = unicode_csv_reader(sys.stdin, fieldnames=fieldnames)
cr = csv.DictReader(sys.stdin, fieldnames=fieldnames)

for row in cr:
    if row['RecType'] == 'RecType':
        continue
    rg_id = row['RGName']

    if rg_id == '':
        continue

    if SUM_SUBSCRIBERS:
        sub_id = 'ALL'
    else:
        sub_id = row['SubscriberID']

    if sub_id not in subs:
        subs[sub_id] = {}

    if rg_id not in subs[sub_id]:
        row['RecType'] = 'summary'
        subs[sub_id][rg_id] = row
        row['SubscriberID'] = sub_id
        row['totalBytes'] = int(row['totalBytes'])
        row['rxBytes'] = int(row['rxBytes'])
        row['txBytes'] = int(row['txBytes'])
        row['TimeDuration'] = int(row['TimeDuration'])
    else:
        subs[sub_id][rg_id]['totalBytes'] += int(row['totalBytes'])
        subs[sub_id][rg_id]['rxBytes'] += int(row['rxBytes'])
        subs[sub_id][rg_id]['txBytes'] += int(row['txBytes'])
        subs[sub_id][rg_id]['TimeDuration'] += int(row['TimeDuration'])

cw = csv.DictWriter(sys.stdout, fieldnames, delimiter=',', quotechar='"',dialect=csv.excel, quoting=csv.QUOTE_ALL)
cw.writeheader()

for sub, rg_rows in subs.iteritems():
    for rg, row in rg_rows.iteritems():
        cw.writerow(row)



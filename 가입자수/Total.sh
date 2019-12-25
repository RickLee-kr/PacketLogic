#!/bin/bash

DATE=`date +%T`
DATE1=`date '+%Y-%m-%d' -d '1 day ago'`
DATE2=`date '+%Y-%m-%d'`

#### TOTAL AS print ####
cd /home/pladmin
/usr/bin/python runScript.py -s "$DATE1 00:00:00" -e "$DATE2 00:00:00" -p "/Netflix_subs?Statistics Object" > /home/pladmin/Scripts/DAY/ToTal_$DATE1.log
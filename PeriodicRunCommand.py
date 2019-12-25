import sys
import string
import time
import datetime
import optparse
from operator import itemgetter
import subprocess

p = optparse.OptionParser(description="Statistics Retriever")
p.add_option("-s", "--start", dest="start", help="Start of search period")
p.add_option("-e", "--end", dest="end", help="End of search period")
p.add_option("-p", "--path", dest="path", help="Statistics Path")

(opt, args) = p.parse_args()

opt.path= "%s"%opt.path
statsPath = opt.path


t1 = datetime.datetime.strptime(opt.start, '%Y-%m-%d %H:%M:%S')
t3 = datetime.datetime.strptime(opt.end, '%Y-%m-%d %H:%M:%S')

temp_st = t1
et = t3

while temp_st<et:

    s = temp_st
    temp_st = temp_st + datetime.timedelta(seconds=300)

    string = '''python NumberOfSubs.py -s "'''+str(s)+'''" -e "'''+str(temp_st)+'''" -p "'''+statsPath+'''" '''
    #print string
    subprocess.Popen(string, shell=True).wait()
    if temp_st > et:
        e = et
    else:
        e = temp_st
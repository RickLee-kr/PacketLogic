#!/usr/bin/env python
# encoding: utf-8
"""
stats-cli-backup.py

Created by Fredrik Johansson on 2012-10-12.
Copyright (c) 2012 Procera Networks. All rights reserved.
"""

import sys
import time
import getopt
import pexpect
import datetime

failed_dates_file = 'failed_dates.txt'


help_message = '''

This script backups up all stats days from day X to day Y. Specify the first and last day and the script will do the rest
(if you have configured CLI remote hosts and stats backup system of course)
You need pexpect installed ("easy_install pexpect")

Usage: script.py -s 2012-01-01 -e 2012-12-31 <-p password -p2 enablepassword>

(-p / -p2 is only needed if you changed the pladmin password, or the "enable" password)
'''

class Usage(Exception):
    def __init__(self, msg):
        self.msg = msg

def daterange(start_date, end_date):
    for n in range(int ((end_date - start_date).days+1)):
        yield start_date + datetime.timedelta(n)

def main(argv=None):
    if argv is None:
        argv = sys.argv
        
    try:
        try:
            opts, args = getopt.getopt(argv[1:], "h:s:e:p:p2", ["hostname=", "startdate=", "enddate=", "password", "enablepassword"])
        except getopt.error, msg:
            raise Usage(msg)
    
        #print opts, args
        # option processing
        for option, value in opts:
            if option in ("-s", "--startdate"):
                startdate = datetime.datetime.strptime(value, "%Y-%m-%d")
            if option in ("-e", "--enddate"):
                enddate = datetime.datetime.strptime(value, "%Y-%m-%d")
            if option in ("-h", "--hostname"):
                hostname = value
            if option in ("-p", "--password"):
                password = value
            if option in ("-p2", "--enablepassword"):
                enablepassword = value
                
        try:
            startdate
        except NameError:
            raise Usage(help_message)
        try:
            enddate
        except NameError:
            raise Usage(help_message)
        try:
            hostname
        except NameError:
            raise Usage(help_message)
        try:
            password
        except NameError:
            password = "pldemo00"
        try:
            enablepassword
        except NameError:
            enablepassword = password
            
            
    except Usage, err:
        print >> sys.stderr, sys.argv[0].split("/")[-1] + ": " + str(err.msg)
        return 2
    
        
#    sys.exit(1)
    SSH = "ssh -p42002 pladmin@%s" % (hostname)
    
    try:
        s = pexpect.spawn (SSH)
    except:
        print "SSH session failed on login."
        print str(s)
        sys.exit(1)


    # Login
    s.expect('Password:')
    s.sendline(password)
    s.expect(' \> ')        
    s.sendline('1')

    # "Enable"
    s.expect('Password:')
    s.sendline(enablepassword)
    s.expect(' \> ')

    # SysAdm
    s.sendline('4')
    s.expect(' \> ')
    
    # Backup
    s.sendline('6')
    s.expect(' \> ')
    
    # Backup statistics
    s.sendline('2')

    # loop through Backup stats single backup
    failed_dates = []
    
    for single_date in daterange(startdate, enddate):

        backupdate = single_date.strftime("%Y-%m-%d")
        
        s.expect('\> ')
        # Single Backup
        s.sendline('2')
        s.expect('\>')

        # S) Specify date to backup
        s.sendline('s')
        s.expect (':',timeout=2)
        
        # Specify date (a to abort): 
        s.sendline(backupdate)
        
        print "Creating statistics backup of", backupdate
        
        i = s.expect (['The day .* does not exist in statistics', 'File uploaded OK'], timeout=120)
        if i == 0:
            failed_dates.append(backupdate)
            print "Error: date %s does not exist" % (backupdate)
            time.sleep(0.5)
            s.sendline('')
            
        if i == 1:
            s.expect('File uploaded OK', timeout=120)
            time.sleep(0.2)    
            s.sendline('')            
    
    # when all is done.    
    print "Done backuping dates from %s to %s " % (startdate.strftime("%Y-%m-%d"), enddate.strftime("%Y-%m-%d"))
    if len(failed_dates) >= 1:
        try:
            f = open(failed_dates_file,'w')
        except:
            print "Cound not write failed dates to file %s" % failed_dates_file
            print "the following dates failed", failed_dates
            sys.exit(1)
        print >>f, "Failed dates for system %s" % hostname
        for date in failed_dates:
            print >>f, date
        print "Failed dates written to %s" % failed_dates_file
        


        
if __name__ == "__main__":
#    sys.exit(main(['./stats-cli-backup.py', '-s', '2012-01-01', '-e', '2012-12-12']))
    sys.exit(main())
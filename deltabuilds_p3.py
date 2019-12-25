#!/usr/bin/env python3

import urllib.request, json
import csv
import datetime, time
import sys, getopt
import os
import re
from operator import methodcaller
from distutils.version import LooseVersion, StrictVersion
import os,sys
import collections

#import distutils

jsondict = [] 
FoundFlag = False
filename = 'BuildDelta' + time.strftime("%Y%m%d%H%M%S") + ".csv"
BASEurl = "http://data.int.prnw.net/systems/src.int.prnw.net/changelogs/firmware/jiraenriched/"

def getDelta (fromVersion, toVersion):
	global FoundFlag
	summary = getJson(BASEurl + "summary.json")
	#od = collections.OrderedDict(sorted(summary.items()))

	fMain, fMajor, fMinor, fBuild = fromVersion.split(".")
	tMain, tMajor, tMinor, tBuild = toVersion.split(".")

	d = sorted(summary, key=lambda x: int(x.split('.')[1]))
	
	for key, value in sorted(summary.items()):
		#print key
		test = key.split(".")
		
		FromMain, FromMajor, FromMinor, FromBuild = test
		
		# PROBLEM todo.
		# 17.2.4.1 -t 17.2.4.11. The FWs are not sorted correctly hence, the output will not be correct.
		#>>> test = { ('17.2.4.0', 0), ('17.2.4.1', 56), ('17.2.4.10', 4), ('17.2.4.11', 1), ('17.2.4.2', 130), ('17.2.4.3', 21), ('17.2.4.4', 130), ('17.2.4.5', 18), ('17.2.4.6', 12), ('17.2.4.7', 14), ('17.2.4.8', 3), ('17.2.4.9', 1), ('17.2.4.next', 33)}

		#do not count the next
		if FromBuild != "next":
			#get the start build, o not count the first build entry ( as it is not part of the delta)
			#if fMain == FromMain and fMajor == FromMajor and fMinor == FromMinor and str(int(fBuild)+1) == FromBuild:
			if fMain == FromMain and fMajor == FromMajor and fMinor == FromMinor and fBuild == FromBuild:
					#build found..
					FoundFlag = True
			

			if tMain == FromMain and tMajor == FromMajor and tMinor == FromMinor and tBuild == FromBuild:
				#make the last entry count..
				
				FoundFlag = False
				url = BASEurl+"BUILD_"+key+".json"
				jsondict.append(getJson(url))
				
		
			#just check that we do nto have a entry that does not exist on major level.
			#and tMajor == FromMajor:
			if FoundFlag == True:

				url = BASEurl+"BUILD_"+key+".json"
				jsondict.append(getJson(url))
						
	return jsondict


def getJson (url):
	response = urllib.request.urlopen(url)
	#raw_html2 = raw_html.replace('\\n', '')
	data = json.loads(response.read())

	return data

def csvwriter (TicketList):
	
	#import csv

	with open(filename, "a", newline='', encoding='utf-8') as csv_file:
		writer = csv.writer(csv_file, delimiter=',')

		for items in TicketList:
			
			for TicketNumber in items:
				
				if TicketNumber:
						try:
							writer.writerow([TicketNumber,items[TicketNumber]['jira']['summary'],items[TicketNumber]['jira']['priority'],items[TicketNumber]['jira']['project']])
						except:
							#if jira key does not exists in JSON (-> NO TICKET and commits not connected to JIRA)
							dictLenght = len(items[TicketNumber]['commits'])

							#iterate over all potential commits
							if TicketNumber != "NO TICKET":
								for i in range(0, dictLenght):					
									writer.writerow([TicketNumber,items[TicketNumber]['commits'][i]['subject']])				
						else:
							continue

def main(argv):
   fromVersion = ''
   toVersion = ''
   try:
      opts, args = getopt.getopt(argv,"hf:t:",["fversion=","tversion="])
   except getopt.GetoptError as err:
      print (err)
      print ("Type -h or --help for help")
      sys.exit(2)
   for opt, arg in opts:
	
      if opt == ('-h', "--help"):
         print ("test.py -f <from version> -o <to version>")
         sys.exit()
      elif opt in ("-f", "--fversion"):
         fromVersion = arg
      elif opt in ("-t", "--tversion"):
         toVersion = arg
   if fromVersion == "" or toVersion == "":
   	if fromVersion == "" and toVersion != "":
   		print ("From version argument: -f/--fversion not specified")
   		sys.exit()   			
   	elif fromVersion != "" and toVersion == "":
   		print ("To version argument: -t/--tversion not specified")
   		sys.exit()
   	else:
   		print ("No argument is specified, please see argument list in -h")
   		sys.exit()

   #check that the pattern of the inparameters are ok..	
   pattern = re.compile("[0-9+].{7}")
   result = pattern.match(fromVersion)
   result2 = pattern.match(toVersion)
   

   if result is None or result2 is None:
   		print ("Incorrect syntaxt of inarguments, should be [x.x.x.x(x)]. Received: from version:", fromVersion, "to version:", toVersion)
   		sys.exit()

   #split the inparameters into variables
   fMain, fMajor, fMinor, fBuild = fromVersion.split(".")
   tMain, tMajor, tMinor, tBuild = toVersion.split(".")

   #continue..
   os.path.dirname(os.path.abspath(__file__))
   currentDirectory = os.getcwd()
 
   #get the delta
   result = getDelta(fromVersion, toVersion)
  
   #write to file..
   csvwriter(result)
   print ("Operation succeeded. File name stored to disk:", filename, "Directory:", currentDirectory)

if __name__ == "__main__":
   main(sys.argv[1:])






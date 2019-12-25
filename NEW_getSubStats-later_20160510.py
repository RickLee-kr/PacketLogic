import packetlogic2
import sys
import string
import time
import datetime
import optparse
from operator import itemgetter

p = optparse.OptionParser(description="Stats Retriever")
p.add_option("-s", "--start", dest="start", help="Start of report period")
p.add_option("-e", "--end", dest="end", help="End of report period")

(opt, args) = p.parse_args()

pl = packetlogic2.connect("127.0.0.1", "admin", "pldemo00")
stat = pl.Statistics()

t1 = datetime.datetime.strptime(opt.start, '%Y-%m-%d %H:%M:%S')
t2 = datetime.datetime.strptime(opt.end, '%Y-%m-%d %H:%M:%S')

output = {}

def clrOutput():
  output['Web Hard'] = (0,0)
  output['P2P'] = (0,0)
  output['Web Browsing'] = (0,0)
  output['Streaming Media'] = (0,0)
  output['SKB VoD'] = (0,0)
  output['SKB VoIP'] = (0,0)

print "Subscriber,\
TotalIn,\
TotalOut,\
WebHardIn,\
WebHardOut,\
P2PIn,\
P2POut,\
StreamingIn,\
StreamingOut,\
WebBrowsingIn,\
WebBrowsingOut,\
B_FreeIn,\
B_FreeOut,\
OthersIn,\
OthersOut"
  
lst1 = stat.list("%s"%t1,"%s"%t2,"/Operation statistics - IP?Statistics Object", pathtype=stat.VALUETYPE_HOST)

for sub in lst1:

  if (len(sub['name']) > 20):
    continue
   
  clrOutput()
 
  try: 
    lst2 = stat.list("%s"%t1,"%s"%t2,"/Operation statistics - IP?Statistics Object/%s?Local Host/Procera Networks Categorization?ServiceObject/Categories?ServiceObject"%sub['name'], pathtype=stat.VALUETYPE_SERVOBJECT)

    for seo2 in lst2:
      if seo2['name']=='Streaming Media':
        output['Streaming Media'] = (int(seo2['values']['bytes in']), int(seo2['values']['bytes out']))

        #try:
          #lst3 = stat.list("%s"%t1,"%s"%t2,"/Operation statistics - Subscribers?Statistics Object/All?NetObject/%s?NetObject/Categories?ServiceObject/Streaming Media?ServiceObject/Video?ServiceObject"%sub['name'], pathtype=stat.VALUETYPE_SERVOBJECT)

          #for seo3 in lst3:
            #if seo3['name']=='SKB VoD':
              #output['SKB VoD'] = (int(seo3['values']['bytes in']), int(seo3['values']['bytes out']))
        #except:
          #pass

      elif seo2['name']=="Web Browsing":
        output['Web Browsing'] = (int(seo2['values']['bytes in']), int(seo2['values']['bytes out']))

      elif seo2['name']=="File Sharing":
        try:
          lst3 = stat.list("%s"%t1,"%s"%t2,"/Operation statistics - IP?Statistics Object/%s?Local Host/Procera Networks Categorization?ServiceObject/Categories?ServiceObject/File Sharing?ServiceObject"%sub['name'], pathtype=stat.VALUETYPE_SERVOBJECT)

          for seo3 in lst3:
            if seo3['name']=='Peer-to-Peer':
              output['P2P'] = (int(seo3['values']['bytes in']), int(seo3['values']['bytes out']))
            elif seo3['name']=='Client-Server':
              output['Web Hard'] = (int(seo3['values']['bytes in']), int(seo3['values']['bytes out']))
              
        except:
          pass 

      elif seo2['name']=='SKB Services':
        try:
          lst3 = stat.list("%s"%t1,"%s"%t2,"/Operation statistics - IP?Statistics Object/%s?Local Host/SKB Serviceses?ServiceObject"%sub['name'], pathtype=stat.VALUETYPE_SERVOBJECT)

          for seo3 in lst3:
            if seo3['name']=='SKB VoD':
              output['SKB VoD'] = (int(seo3['values']['bytes in']), int(seo3['values']['bytes out']))
            elif seo3['name']=='SKB VoIP':
              output['SKB VoIP'] = (int(seo3['values']['bytes in']), int(seo3['values']['bytes out']))
        except:
          pass
  except:
    pass
          
  bytesIn = 0
  bytesOut = 0
  
  for cat in output:
    if cat not in ['SKB VoD']:
      bytesIn += output[cat][0]
      bytesOut += output[cat][1]
    
  print "%s,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d" % (
    sub['name'],
    sub['values']['bytes in'],
    sub['values']['bytes out'],
    output['Web Hard'][0],
    output['Web Hard'][1],
    output['P2P'][0],
    output['P2P'][1],
    output['Streaming Media'][0],
    output['Streaming Media'][1],
    output['Web Browsing'][0],
    output['Web Browsing'][1],
    output['SKB VoD'][0]+output['SKB VoIP'][0],
    output['SKB VoD'][1]+output['SKB VoIP'][1],
    sub['values']['bytes in']-bytesIn,
    sub['values']['bytes out']-bytesOut)

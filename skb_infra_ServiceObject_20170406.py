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

pl = packetlogic2.connect("58.123.218.35", "admin", "smartwjdqh")
stat = pl.Statistics()

t1 = datetime.datetime.strptime(opt.start, '%Y-%m-%d %H:%M:%S')
t2 = datetime.datetime.strptime(opt.end, '%Y-%m-%d %H:%M:%S')

output = {}

def clrOutput():
  output['Web Hard'] = (0,0)
  output['P2P'] = (0,0)
  output['Web Browsing'] = (0,0)
  output['Streaming Media'] = (0,0)
  output['File Transfer'] = (0,0)
  output['Business Systems'] = (0,0)
  output['Entertainment'] = (0,0)
  output['Messaging and Collaboration'] = (0,0)
  output['Network Infrastructure'] = (0,0)
  output['Remote Access'] = (0,0)
  output['Malware'] = (0,0)
  output['Information'] = (0,0)
  output['IP Protocols'] = (0,0)
  output['SK Btv'] = (0,0)
  output['SKB VoD'] = (0,0)
  output['SKB VoIP'] = (0,0)
  

print "Subscriber,\
TotalIn,\
TotalOut,\
WebHardIn,\
WebHardOut,\
P2PIn,\
P2POut,\
WebBrowsingIn,\
WebBrowsingOut,\
StreamingIn,\
StreamingOut,\
FileTransferIn,\
FileTransferOut,\
BusinessSystemsIn,\
BusinessSystemsOut,\
EntertainmentIn,\
EntertainmentOut,\
MessagingandCollaborationIn,\
MessagingandCollaborationOut,\
NetworkInfrastructureIn,\
NetworkInfrastructureOut,\
RemoteAccessIn,\
RemoteAccessOut,\
MalwareIn,\
MalwareOut,\
InformationIn,\
InformationOut,\
IPProtocolsIn,\
IPProtocolsOut,\
SKBtvIn,\
SKBtvOut,\
SKBVoDIn,\
SKBVoDOut,\
SKBVoIPIn,\
SKBVoIPOut,\
OthersIn,\
OthersOut"
  
lst1 = stat.list("%s"%t1,"%s"%t2,"/Subscribers?Statistics Object", pathtype=stat.VALUETYPE_HOST)

for sub in lst1:

  if (len(sub['name']) > 20):
    continue
   
  clrOutput()
 
  try: 
    lst2 = stat.list("%s"%t1,"%s"%t2,"/Subscribers?Statistics Object/%s?Local Host/Procera Networks Categorization?ServiceObject/Categories?ServiceObject"%sub['name'], pathtype=stat.VALUETYPE_SERVOBJECT)

    for seo2 in lst2:
      if seo2['name']=='Streaming Media':
        output['Streaming Media'] = (int(seo2['values']['bytes in']), int(seo2['values']['bytes out']))

      elif seo2['name']=="Web Browsing":
        output['Web Browsing'] = (int(seo2['values']['bytes in']), int(seo2['values']['bytes out']))

      elif seo2['name']=="File Transfer":
        output['File Transfer'] = (int(seo2['values']['bytes in']), int(seo2['values']['bytes out']))
        
      elif seo2['name']=="Business Systems":
        output['Business Systems'] = (int(seo2['values']['bytes in']), int(seo2['values']['bytes out']))

      elif seo2['name']=="Entertainment":
        output['Entertainment'] = (int(seo2['values']['bytes in']), int(seo2['values']['bytes out']))

      elif seo2['name']=="Messaging and Collaboration":
        output['Messaging and Collaboration'] = (int(seo2['values']['bytes in']), int(seo2['values']['bytes out']))

      elif seo2['name']=="Network Infrastructure":
        output['Network Infrastructure'] = (int(seo2['values']['bytes in']), int(seo2['values']['bytes out']))
        
      elif seo2['name']=="Remote Access":
        output['Remote Access'] = (int(seo2['values']['bytes in']), int(seo2['values']['bytes out']))

      elif seo2['name']=="Malware":
        output['Malware'] = (int(seo2['values']['bytes in']), int(seo2['values']['bytes out']))

      elif seo2['name']=="Information":
        output['Information'] = (int(seo2['values']['bytes in']), int(seo2['values']['bytes out']))

      elif seo2['name']=="IP Protocols":
        output['IP Protocols'] = (int(seo2['values']['bytes in']), int(seo2['values']['bytes out']))

      elif seo2['name']=="File Sharing":
        try:
          lst3 = stat.list("%s"%t1,"%s"%t2,"/Subscribers?Statistics Object/%s?Local Host/Procera Networks Categorization?ServiceObject/Categories?ServiceObject/File Sharing?ServiceObject"%sub['name'], pathtype=stat.VALUETYPE_SERVOBJECT)

          for seo3 in lst3:
            if seo3['name']=='Peer-to-Peer':
              output['P2P'] = (int(seo3['values']['bytes in']), int(seo3['values']['bytes out']))
            elif seo3['name']=='Client-Server':
              output['Web Hard'] = (int(seo3['values']['bytes in']), int(seo3['values']['bytes out']))
              
        except:
          pass 

      elif seo2['name']=='SKB Serviceses':
        try:
          lst4 = stat.list("%s"%t1,"%s"%t2,"/Subscribers?Statistics Object/%s?Local Host/Procera Networks Categorization?ServiceObject/Categories?ServiceObject/SKB Serviceses?ServiceObject"%sub['name'], pathtype=stat.VALUETYPE_SERVOBJECT)

          for seo4 in lst4:
            if seo4['name']=='SKB VoD':
              output['SKB VoD'] = (int(seo4['values']['bytes in']), int(seo4['values']['bytes out']))
            elif seo4['name']=='SKB VoIP':
              output['SKB VoIP'] = (int(seo4['values']['bytes in']), int(seo4['values']['bytes out']))
            elif seo4['name']=='SK Btv':
              output['SK Btv'] = (int(seo4['values']['bytes in']), int(seo4['values']['bytes out']))
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
    
  print "%s,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d" % (
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
    output['File Transfer'][0],
    output['File Transfer'][1],
    output['Business Systems'][0],
    output['Business Systems'][1],
    output['Entertainment'][0],
    output['Entertainment'][1],
    output['Messaging and Collaboration'][0],
    output['Messaging and Collaboration'][1],
    output['Network Infrastructure'][0],
    output['Network Infrastructure'][1],
    output['Remote Access'][0],
    output['Remote Access'][1],
    output['Malware'][0],
    output['Malware'][1],
    output['Information'][0],
    output['Information'][1],
    output['IP Protocols'][0],
    output['IP Protocols'][1],
    output['SK Btv'][0],
    output['SK Btv'][1],
    output['SKB VoD'][0],
    output['SKB VoD'][1],
    output['SKB VoIP'][0],
    output['SKB VoIP'][1],
    sub['values']['bytes in']-bytesIn,
    sub['values']['bytes out']-bytesOut)

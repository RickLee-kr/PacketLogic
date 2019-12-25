import packetlogic2 as pl2
import sys
import csv
import os
import time
import tarfile

# Connect to the local PacketLogic and SystemDiagnostics
c = pl2.connect("127.0.0.1", "admin", "pldemo00")
s = c.SysDiag()

# Create the output directory if running for the first time
if not os.path.exists("/tmp/rxdrops-logs"):
  os.makedirs("/tmp/rxdrops-logs")

# Get current date and time, open a log file to be written and destination tarball
date = time.strftime("%Y-%m-%d.%X", time.localtime())
out = open("/tmp/rxdrops-logs/" + date + ".log", "w")
tarout = tarfile.open("/tmp/rxdrops-logs/" + date + ".tar.gz", "w:gz")

# Write all SystemDiagnostics zones values to the file
zone_list = s.zone_list()
if zone_list:
  w = csv.DictWriter(out, ["zone", "level", "value", "min", "max", "rate"])
  w.writeheader()
  for z in zone_list.values():
    for vd in sorted(z.valuedefs.values(), key=lambda vd: "/".join(vd.value.level)):
      v = vd.value
      w.writerow({"zone": z.name, "level": "/".join(v.level), "value": v.value, "min": v.min, "max": v.max, "rate": v.rate})
      w.writerows([{"zone": z.name, "level": "/".join(vv.level), "value": vv.value, "min": vv.min, "max": vv.max, "rate": vv.rate} for vv in sorted(vd.values(), key=lambda v: "/".join(v.level))])
else:
  print >> sys.stderr, "Zone list empty"

# Tar the log file and close the tarball
tarout.add("/tmp/rxdrops-logs/" + date + ".log")
tarout.close()

# Remove the log file
os.remove("/tmp/rxdrops-logs/" + date + ".log")

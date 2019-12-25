#!/usr/bin/python

import packetlogic2

import traceback
import optparse
import sys

p = optparse.OptionParser(description="Stats Retriever")
p.add_option("-s", "--start", dest="start", help="Start of report period")
p.add_option("-e", "--end", dest="end", help="End of report period")
p.add_option("-t", "--timeout", dest="timeout", help="Timeout on the connection to stats")
p.add_option("-S", "--subscriber", dest="subscriber", help="Single subscriber to do search on")
p.add_option("-p", "--pretty", dest="pretty", action="store_true", help="Pretty print output?")


HOST = "192.168.0.10"
USER = "admin"
PASS = "pldemo00"

# default timeout in seconds
TIMEOUT = 60

PRINTORDER = [
    {"key": "Subscriber", "header": "Subscriber"},
    {"key": "Total", "header": "Total"},
    {"key": "Web Hard", "header": "WebHard", "in": 0, "out": 0},
    {"key": "P2P", "header": "P2P", "in": 0, "out": 0},
    {"key": "Streaming Media", "header": "Streaming", "in": 0, "out": 0},
    {"key": "Web Browsing", "header": "WebBrowsing", "in": 0, "out": 0},
    {"key": "SKB VoD", "header": "SKBVod", "in": 0, "out": 0},
    {"key": "SKB VoIP", "header": "SKBVoIP", "in": 0, "out": 0},
    {"key": "Others", "header": "Others"}
]

def get_stats(stat, opt):

    starttime = opt.start
    endtime = opt.end
    subscriberId = opt.subscriber

    if subscriberId:
        print "Executing query between %s and %s on subscriber %s" % (starttime, endtime, subscriberId)
    else:
        print "Executing query between %s and %s on all subscribers" % (starttime, endtime)

    if not subscriberId:
        print "Getting all subscribers..."
        subscribers = stat.list(starttime, endtime, "/Subscribers?Statistics Object/")
        print "Done. Collecting statistics from each subscriber, please wait..."
    else:
        sub = stat.transfer_get(starttime, endtime, "/Subscribers?Statistics Object/%s?NetObject" % subscriberId)
        sub['name'] = subscriberId
        subscribers = [sub]

    print ""

    picdata = []
    for sub in subscribers:
        res = extract_stats(sub, starttime, endtime)
        if res:
            picdata.append(res)

    if not picdata:
        print "Could not extract any data."
        return

    print "RESULT:"

    if opt.pretty:
        for data in picdata:
            for printdata in PRINTORDER:
                key = printdata["key"]
                if key == "Subscriber":
                    print "%s: %s" % (printdata["header"], data[key]["value"])
                else:
                    print "%sIn: %s" % (printdata["header"], str(data[key]["in"]))
                    print "%sOut: %s" % (printdata["header"], str(data[key]["out"]))
    else:
        # print header
        buff = []
        for printdata in PRINTORDER:
            if printdata["key"] == "Subscriber":
                buff.append(printdata["header"])
            else:
                buff.append(printdata["header"] + "In")
                buff.append(printdata["header"] + "Out")
        print ",".join(buff)

        for data in picdata:
            # sort extracted pic data by sortorder
            buff = []
            for printdata in PRINTORDER:
                key = printdata["key"]
                if key == "Subscriber":
                    buff.append(data[key]["value"])
                else:
                    buff.append(data[key]["in"])
                    buff.append(data[key]["out"])
            buff = map(str, buff)
            print ",".join(buff)


def extract_stats(sub, starttime, endtime):
        try:
            aid = sub['name']
            if (len(aid) != 10) or "." in aid:
                return

            netobjects = stat.list(starttime, endtime, "/Subscribers?Statistics Object/%s?NetObject/" % aid)

            # what we want to extract from PIC
            output = {
                "Web Hard": {"in": 0, "out": 0},
                "P2P": {"in": 0, "out": 0},
                "Streaming Media": {"in": 0, "out": 0},
                "Web Browsing": {"in": 0, "out": 0},
                "SKB VoD": {"in": 0, "out": 0},
                "SKB VoIP": {"in": 0, "out": 0},
            }

            for netobject in netobjects:
                service_name = netobject['name']
                if service_name == "File Sharing":
                    filesharing_stats = stat.list(starttime, endtime, "/Subscribers?Statistics Object/%s?NetObject/%s?ServiceObject/" % (aid, service_name))
                    for record in filesharing_stats:
                        if record['name'] == "Peer-to-Peer":
                            output['P2P']['in'] += record['values']['bytes in']
                            output['P2P']['out'] += record['values']['bytes out']
                        elif record['name'] == "Client-Server":
                            output['Web Hard']['in'] += record['values']['bytes in']
                            output['Web Hard']['out'] += record['values']['bytes out']
                elif service_name in output:
                    output[service_name]['in'] += netobject['values']['bytes in']
                    output[service_name]['out'] += netobject['values']['bytes out']

            totalIn = int(sub['values']['bytes in'])
            totalOut = int(sub['values']['bytes out'])

            # Calculate 'Others' which is total minus services defined in output
            otherIn = totalIn
            otherOut = totalOut
            for key in output:
                otherIn -= int(output[key]["in"])
                otherOut -= int(output[key]["out"])


            # add other to output dict
            output["Others"] = {
                "in": otherIn,
                "out": otherOut
            }

            # add subscriber name
            output["Subscriber"] = {
                "value": aid
            }

            output["Total"] = {
                "in": totalIn,
                "out": totalOut
            }

            return output

        except Exception, e:
            print "Error executing search on %s. Cause: %s" % (aid, str(e))
            print traceback.format_exc()


if __name__ == "__main__":
    (opt, args) = p.parse_args()

    if not opt.start or not opt.end:
        sys.exit("Must pass --start and --end")

    if opt.timeout:
        TIMEOUT = opt.timeout

    print "Connecting to %s with timeout %s, please wait..." % (HOST, TIMEOUT)
    pl = packetlogic2.connect(host=HOST, username=USER, password=PASS, timeout=float(TIMEOUT))

    stat = pl.Statistics()

    get_stats(stat, opt)


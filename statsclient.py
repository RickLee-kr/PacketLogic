from collections import namedtuple
import datetime
import re
import packetlogic2


StatsInterval = namedtuple('StatsInterval', 'start_date end_date start_str end_str')


class StatsClient(object):
    def __init__(self, host, user, password, timeout=60):
        self.hostname = host
        self.username = user
        self.password = password
        self.timeout = timeout
        self.pl = None
        self.stats = None

    def _connect(self):
        self.pl = packetlogic2.connect(self.hostname, self.username, self.password, timeout=self.timeout)
        self.stats = self.pl.Statistics()
        self.stats.timeout = self.timeout
        self.tz_offset = self._tz_offset()

    def _tz_offset(self):
        so = self.pl.SystemOverview()
        systems = so.system_list()
        matched = [s for s in systems if s.systemid == so.systemid]

        if len(matched) != 1:
            raise RuntimeError("Could not find myself (%s)" % so.systemid)

        ts = matched[0].lastupdate
        m = re.match('[0-9-]+\s+[0-9:]+([+-]\d+)', ts)

        if not m:
            raise RuntimeError("Could not extract time zone from '%s'" % me.lastupdate)

        return 3600 * int(m.group(1))

    def _get_graph(self, startdate, enddate, statpath, items):
        result = {'in': [], 'out': [], 'tot': []}
        try:
            graph = self.stats.graph(startdate, enddate, statpath, items, mode=2)
            for dp in graph:
                result['in'].append([dp.get('timestamp') - self.tz_offset, int(dp.get('bytes in')) * 8])
                result['out'].append([dp.get('timestamp') - self.tz_offset, int(dp.get('bytes out')) * 8])
                result['tot'].append([dp.get('timestamp') - self.tz_offset, int(dp.get('bytes total')) * 8])

        except Exception, e:
            print("EXCEPTION: %s" % e)
            result = {'in': [], 'out': [], 'tot': []}
        finally:
            return result

    def _get_list(self, startdate, enddate, statpath, statstype, maxitems=10):
        result = []
        try:
            statslist = self.stats.list(startdate, enddate, statpath)
            for item in statslist:
                if item.get('type') != statstype:
                    continue
                result.append([int(item.get('values').get('bytes total')),
                               str(item.get('name'))])

            result = sorted(result, key=lambda i: -i[0])
            result = result[:maxitems]

        except Exception, e:
            print("EXCEPTION: %s" % e)
            result = []
            self.close()
        finally:
            return result

    def _interval(self, hours):
        date_end = datetime.datetime.utcnow() + datetime.timedelta(seconds=self.tz_offset)
        date_end_str = date_end.strftime("%Y-%m-%d %H:%M")

        date_start = date_end - datetime.timedelta(hours=hours)
        date_start_str = date_start.strftime("%Y-%m-%d %H:%M")

        return StatsInterval(date_start, date_end, date_start_str, date_end_str)

    def get_traffic(self, path, hours, items):
        if not self.pl:
            self._connect()

        intv = self._interval(hours)
        d = self._get_graph(intv.start_str, intv.end_str, path, items)

        return d

    def get_services(self, path, hours, items=10):
        if not self.pl:
            self._connect()

        intv = self._interval(hours)
        d = self._get_list(intv.start_str, intv.end_str, path, self.stats.VALUETYPE_SERVICE, items)

        return d

    def close(self):
        if self.pl:
            self.stats.close()
            self.pl = None

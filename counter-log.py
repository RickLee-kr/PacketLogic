# standard
import time
import Queue
import threading
import datetime
import os
import os.path
import thread

def update(idx = None, last = None, sobj = None, splitk = None, in_delta = None, out_delta = None, msg = None):
	return (time.time(), idx, last, sobj, splitk, in_delta, out_delta, msg)

def filterNone(v):
	return str(v) if v is not None else ""

def quote(s):
	return s.replace("\"", "\"\"")

def formatUpdate(update):
	return ("%0.3f," % update[0]) + ",".join(quote(filterNone(v)) for v in update[1:]) + "\n"

class LogWriter(object):
	def __init__(self, limit, p, filename, ext, header=None):
		self.path = p
		self.filename = filename
		self.ext = ext
		self.limit = limit
		self.file = None
		self.last_flush = None
		self.header = header

		self._rotate()

	def next_name(self, index):
		if index == 0:
			return os.path.join(self.path, "%s.%s" % (self.filename, self.ext))
		return os.path.join(self.path, "%s.%d.%s" % (self.filename, index - 1, self.ext))

	def _rename(self, n):
		src = self.next_name(n)
		if os.path.exists(src):
			dst = self.next_name(n + 1)
			if os.path.exists(dst):
				self._rename(n + 1)
			os.rename(src, dst)

	def _flush(self, now):
		self.file.flush()
		self.last_flush = now

	def _writeline(self, line):
		self.lines = self.lines + 1
		self.file.write(line)

	def _rotate(self):
		if self.file:
			self.file.close()
		self._rename(0)
		self.file = open(self.next_name(0), "w")
		self.lines = 0

		if self.header:
			self._writeline(self.header)
		self._flush(time.time())

	def tick(self):
		now = time.time()
		if now - self.last_flush > 5:
			self._flush(now)

	def write(self, line):
		if self.lines >= self.limit:
			self._rotate()
		self._writeline(line)

	def close(self):
		self.file.close()

class DiffCounter(object):
	__slots__ = ('idx', 'oid', 'splitk', '_in', '_out')
	def __init__(self, idx):
		self.idx = idx
		self._reset()

	def _reset(self):
		self.oid = None
		self.splitk = None
		self._in = 0
		self._out = 0

	def _apply(self, _in, _out):
		msg = None

		in_diff = _in - self._in
		out_diff = _out - self._out

		if not (0 <= in_diff < 1000000000 and 0 <= out_diff < 1000000000) or (in_diff == 0 and out_diff == 0):
			msg = "Suspicious counter update; in: %d -> %d = %d, out: %d -> %d = %d" % (self._in, _in, in_diff, self._out, _out, out_diff)
			in_diff = None
			out_diff = None

		self._in = _in
		self._out = _out

		return (in_diff, out_diff, msg)

	def update(self, oid, splitk, last, _in, _out):
		if self.oid is None:
			if last:
				# No sanity checking since we have nothing to compare against
				return (_in, _out, "Unbased last update")
			self.oid = oid
			self.splitk = splitk
			self._in = _in
			self._out = _out
			return (_in, _out, "Baseline")

		if oid != self.oid or splitk != self.splitk:
			msg = "Unexpected counter meta-data; oid: %s, splitkey: %s, %d -> %d, out: %d -> %d" % (oid, splitk, self._in, _in, self._out, _out)
			self.oid = oid
			self.splitk = splitk
			self._in = _in
			self._out = _out
			return (None, None, msg)

		diff = self._apply(_in, _out)

		# Next update of this counter should start at 0
		if last:
			self._reset()
		return diff

class PLCounterReaper (threading.Thread):

	def __init__ (self, pl, callback):
		threading.Thread.__init__(self)
		self.pl = pl
		self.cb = callback
		self.rt = None
		self.instanceid = None
		self.counters = {}
		self.fetching_baseline = False
		self.sobjs = {}

	def run (self):
		while True:
			try:
				self._connect()
				self.rt.update_forever()
			except IOError:
				self.cb(update(msg = "Connection failed, retrying soon"))
				time.sleep(10)

	def _connect (self):
		if not self.rt is None:
			self.rt.close()
			self.rt = None
		self.rt = self.pl.Realtime()
		rs = self.pl.Ruleset()

		self.cb(update(msg="Connected to %s at %s as %s (%s)" % (self.rt.systemid, self.rt.host, self.rt.user, self.rt.distversion)))

		config = self.pl.Config()
		for c in ["SHAPING_COUNTERS_GRANULARITY_SHIFT", "SHAPING_COUNTERS_MAX", "SHAPING_COUNTERS_SUBSCRIBER_SEND_ALL"]:
			self.cb(update(msg="Config %s = %s" % (c, config.get(c)["value"])))

		self.sobjs = dict((so.id, so.name) for so in rs.shapingobject_list())

		instanceid = self.rt.instanceid
		if self.instanceid and self.instanceid != instanceid:
			self.cb(update(msg = "pl instance has changed, we may have lost data"))
			# but on the other hand we can use absolute values
			self.fetching_baseline = False
			self.counters = {}
		else:
			self.cb(update(msg = "Fetching previous values"))
			# we need to grab an baseline to calculate relative values from
			self.fetching_baseline = True
			self.counters = {}

		self.instanceid = instanceid
		self.rt.add_shapingcnt_callback(self.update)

		if self.fetching_baseline:
			self.rt.shapingcnt_request_all()
			self.rt.add_update_done_callback(self.update_done)

	def update_done(self):
		if self.fetching_baseline:
			self.cb(update(msg = "Previous values fetched"))
		self.fetching_baseline = False

	def update(self, idx, oid, splitk, flags, _in, _out):
		last = bool(flags & (1 << 13))

		c = self.counters.get(idx)
		if c is None:
			self.counters[idx] = c = DiffCounter(idx)

		diff = c.update(oid, splitk, last, _in, _out)

		if diff:
			_in, _out, msg = diff
			sobj = self.sobjs.get(oid, '<unknown>')
			self.cb(update(idx, "LAST" if last else None, sobj, splitk, _in, _out, msg))

def start (pl):
	queue  = Queue.Queue()
	reaper = PLCounterReaper(pl, queue.put)
	reaper.setDaemon(True)
	reaper.start()
	return queue


if __name__ == '__main__':
	import packetlogic2
	import sys

	h,u,p, lp = sys.argv[1:]
	counterWriter = LogWriter(2000000, lp, "counter-values", "log", header="timestamp,index,flags,shaping_object,splitkey,in,out,msg\n")
	pl = packetlogic2.connect(h,u,p)
	try:
		q = start(pl)

		while True:
			try:
				e = q.get(timeout=1)
				counterWriter.write(formatUpdate(e))
			except Queue.Empty:
				counterWriter.tick()
	finally:
		counterWriter.close()

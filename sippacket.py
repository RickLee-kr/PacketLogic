""" Who came up with the extremely brilliant idea to have short versions of
header names? """
headerconv = {	"i": "call-id",
		"m": "contact",
		"e": "content-encoding",
		"l": "content-length",
		"c": "content-type",
		"f": "from",
		"s": "subject",
		"t": "to",
		"v": "via",
	     }

class SIPPacket:
	def __init__(self, packet):
		"""Fill info from supplied binary packet data."""
		self.type = 'UNKNOWN'
		self.sipversion = self.code = self.reason = self.requesturi = ''
		self.method = ''

		try:
			self._parseSIP(packet)
		except:
			raise

		if self.reqstat[0].upper().startswith("SIP/"):
			self.type = 'RESPONSE'
			self.sipversion = self.reqstat[0].strip().upper()
			self.code = self.reqstat[1].strip().upper()
			self.reason = self.reqstat[2].strip()
		else:
			self.type = 'REQUEST'
			self.method = self.reqstat[0].strip().upper()
			self.requesturi = self.reqstat[1].strip()
			self.sipversion = self.reqstat[2].strip().upper()

		if self.sipversion != "SIP/2.0":
			raise ValueError("Bad SIP version")

	def _parseSIP(self, packet):
		"""Parse SIP packet to a nice structure.
		Supports multiple occurances of the same header,
		multi line headers."""

		self.header = {}
		self.body = ''
		self.reqstat = []
		key = ''
		leftover = packet

		while leftover:
			data = leftover.split('\n', 1)
			if len(data) < 2:
				raise ValueError("Not enough rows")
			line = data[0].replace("\r", "")
			leftover = data[1]

			if not line:
				if not key:	# no headers yet, skip this empty line
					#print("Skipping empty row before headers")
					continue
				self.body = leftover
				break
			if not self.reqstat:
				data = line.split(None, 2)
				if len(data) < 3:
					raise ValueError("Too few columns in request/status message")
				self.reqstat = data
				continue
			if line[0].isspace():	# Multi line header, add this line to the previous header
				if not key:	# huh? multiline header without previous header? wtf!
					#print("Looked like multi line header but it was crap, skipping")
					continue
				self.header[key] += " " + line.lstrip()
				#print("Multi line header, appending to previous header")
				continue
		
			data = line.split(':', 1)
			if len(data) < 2:
				#print("Broken header line? skipping")
				continue	# broken header line?
			data[0].strip()
			if data[0].find(" ") != -1 or data[0].find("\t") != -1:
				#print("Whitespace in key, skipping")
				continue
			key = data[0].lower()
			val = data[1]

			key = headerconv.get(key, key)
			if key in self.header:
				self.header[key] += "," + val
			else:
				self.header[key] = val

		for key, val in self.header.iteritems():
			self.header[key] = [line.strip() for line in val.split(',')]



UNIVERSAL = 0x0
APPLICATION = 0x40
CONTEXT_SPECIFIC = 0x80
PRIVATE = 0xc0

BOOLEAN = 0x01
INTEGER = 0x02
BIT_STRING = 0x03
OCTET_STRING = 0x04
OBJECT_IDENTIFIER = 0x06
ENUMERATED = 0x0A
SEQUENCE = 0x10
SET = 0x11

def decodeInteger(data):
    return reduce(lambda x, y: (x << 8) | ord(y), data, 0)

def decodeHex(data):
    return "".join("%02x" % ord(d) for d in data)

class Buffer(object):
    def __init__(self, data):
        self.data = data
        self.pos = 0
    def get(self, length):
        if self.pos + length > len(self.data):
            raise IOError("Not enough bytes remaining: %d" % length)
        self.pos += length
        return self.data[self.pos-length:self.pos]
    def getByte(self):
        return ord(self.get(1))
    def advance(self, cnt):
        if self.pos + cnt > len(self.data):
            raise IOError("Not enough bytes remaining: %d" % cnt)
        self.pos += cnt
        return Buffer(self.data[self.pos-cnt:self.pos])
    def mark(self):
        self.saved = self.pos
    def reset(self):
        self.pos = self.saved
    def hasRemaining(self):
        return self.pos < len(self.data)

class DERParser(object):
    def __init__(self, buf):
        self.buf = buf

    def hasRemaining(self):
        return self.buf.hasRemaining()

    def whileRemaining(self):
        while self.hasRemaining():
            yield self

    def decodeBase128(self):
        result = 0
        for i in xrange(0, 5):
            b = self.buf.getByte()
            result = (result << 7) | (b & 0x7f)
            if ((b & 0x80) == 0):
                return result
        raise IOError("To many bytes in base128 value")

    def decodeLength(self):
        c = self.buf.getByte()
        if c & 0x80 == 0:
            return c
        return decodeInteger(self.buf.get(c & 0x7f))

    def getTag(self):
        c = self.buf.getByte()
        constructed = (c & 0x20) != 0
        cls = c & 0xc0
        tagNo = c & 0x1F
        if tagNo >= 0x1F:
            tagNo = self.decodeBase128()
        return tagNo, cls, constructed

    def getBoolean(self):
        if self.decodeLength() != 1:
            raise IOError("Invalid boolean length: %d" % l)
        return self.buf.getByte() != 0

    def getInteger(self):
        data = self.buf.get(self.decodeLength())
        if len(data) > 8:
            raise IOError("To many bytes for integer: %d" % l)
        return decodeInteger(data)

    def getEnumerated(self):
        return self.getInteger()

    def getString(self):
        return self.buf.get(self.decodeLength())

    def getHex(self):
        data = self.buf.get(self.decodeLength())
        return decodeHex(data)

    def getOid(self):
        result = []
        l = self.decodeLength()
        limit = self.buf.pos + l
        c = self.buf.getByte()
        result.append(c / 40)
        result.append(c % 40)
        while self.buf.pos < limit:
            result.append(self.decodeBase128())
        return '.'.join(str(x) for x in result)

    def getSequence(self):
        return DERParser(self.buf.advance(self.decodeLength()))

    def getSet(self):
        return self.getSequence()

    def getChoice(self):
        return self.getSequence()

    def optionalTag(self, tagNoEx, clsEx=CONTEXT_SPECIFIC):
        self.buf.mark()
        tagNo, cls, constructed = self.getTag()
        if tagNo == tagNoEx and cls == clsEx:
            return True
        self.buf.reset()
        return False

    def expectTag(self, tagNoEx, clsEx=CONTEXT_SPECIFIC):
        tagNo, cls, constructed = self.getTag()
        if tagNo != tagNoEx:
            raise IOError("Expected tag nr %d but got %d" % (tagNoEx, tagNo))
        if cls != clsEx:
            raise IOError("Expected class %d but got %d" % (clsEx, cls))

    def getBooleanTag(self, tagNo=None, cls=CONTEXT_SPECIFIC):
        if tagNo is None:
            tagNo, cls = BOOLEAN, UNIVERSAL
        self.expectTag(tagNo, cls)
        return self.getBoolean()

    def getIntegerTag(self, tagNo=None, cls=CONTEXT_SPECIFIC):
        if tagNo is None:
            tagNo, cls = INTEGER, UNIVERSAL
        self.expectTag(tagNo, cls)
        return self.getInteger()

    def getIntegerTag(self, tagNo=None, cls=CONTEXT_SPECIFIC):
        if tagNo is None:
            tagNo, cls = INTEGER, UNIVERSAL
        self.expectTag(tagNo, cls)
        return self.getInteger()

    def getEnumeratedTag(self, tagNo=None, cls=CONTEXT_SPECIFIC):
        if tagNo is None:
            tagNo, cls = ENUMERATED, UNIVERSAL
        self.expectTag(tagNo, cls)
        return self.getEnumerated()

    def getStringTag(self, tagNo=None, cls=CONTEXT_SPECIFIC):
        if tagNo is None:
            tagNo, cls = OCTET_STRING, UNIVERSAL
        self.expectTag(tagNo, cls)
        return self.getString()

    def getSequenceTag(self, tagNo=None, cls=CONTEXT_SPECIFIC):
        if tagNo is None:
            tagNo, cls = SEQUENCE, UNIVERSAL
        self.expectTag(tagNo, cls)
        return self.getSequence()

    def getSetTag(self, tagNo=None, cls=CONTEXT_SPECIFIC):
        if tagNo is None:
            tagNo = SET
            cls = UNIVERSAL
        self.expectTag(tagNo, cls)
        return self.getSet()

    def getOidTag(self, tagNo=None, cls=CONTEXT_SPECIFIC):
        if tagNo is None:
            tagNo, cls = OBJECT_IDENTIFIER, UNIVERSAL
        self.expectTag(tagNo, cls)
        return self.getOid()

    def getChoiceTag(self, tagNo, cls=CONTEXT_SPECIFIC):
        self.expectTag(tagNo, cls)
        return self.getChoice()

def noformat(x):
    return x

CLOSE_CAUSES={0:'normalRelease', 4:'abnormalRelease', 16:'volumeLimit', 17:'timeLimit', 18:'servingNodeChange', 20:'managementIntervention'}
def formatCloseCause(cc):
    return CLOSE_CAUSES.get(cc, 'unknown/invalid')

PDPTYPES = {0x0121: 'ipv4', 0x0157: 'ipv6', 0x018d: 'ipv4v6', 0x0001: 'ppp'}
def formatPdpType(pt):
    return PDPTYPES.get(decodeInteger(pt), 'unknown')

def formatTimestamp(ts):
    if len(ts) != 9:
        raise IOError("Timestamp length is not 9: %s" % ts)
    ts = [ord(x) for x in ts]
    year = 10 * ((ts[0] >> 4) & 0x0f) + (ts[0] & 0x0f) + 2000
    month = 10 * ((ts[1] >> 4) & 0x0f) + (ts[1] & 0x0f)
    day = 10 * ((ts[2] >> 4) & 0x0f) + (ts[2] & 0x0f)
    hour = 10 * ((ts[3] >> 4) & 0x0f) + (ts[3] & 0x0f)
    minute = 10 * ((ts[4] >> 4) & 0x0f) + (ts[4] & 0x0f)
    second = 10 * ((ts[5] >> 4) & 0x0f) + (ts[5] & 0x0f)
    sgnTz = chr(ts[6])
    ofsHours = 10 * ((ts[7] >> 4) & 0x0f) + (ts[7] & 0x0f)
    ofsMinutes = 10 * ((ts[8] >> 4) & 0x0f) + (ts[8] & 0x0f)
    return "%04d-%02d-%02dT%02d:%02d:%02d%s%02d:%02d" % (year, month, day, hour, minute, second, sgnTz, ofsHours, ofsMinutes)

def formatMccMnc(mccmnc):
    mccmnc = [ord(x) for x in mccmnc]
    result = []
    result.append((mccmnc[0] & 0x0F))
    result.append((mccmnc[0] & 0xF0) >> 4)
    result.append((mccmnc[1] & 0x0F))
    result.append((mccmnc[2] & 0x0F))
    result.append((mccmnc[2] & 0xF0) >> 4)
    result.append((mccmnc[1] & 0xF0) >> 4)
    result = filter(lambda x : (x >= 0) and (x <= 9), result)
    result = ''.join(chr(x + ord('0')) for x in result)
    return result

def formatBCD(bcd):
    result = 0
    for x in bcd:
        for d in [(ord(x) >> 4) & 0xF, ord(x) & 0xF]:
            if d < 10:
                result = result * 10 + d
    return result

def formatMSISDN(msisdn):
    return formatBCD(msisdn[1:])

def getHex(p):
    return p.getHex()
def getString(p):
    return p.getString()
def getInteger(p):
    return p.getInteger()
def getEnumerated(p):
    return p.getInteger()
def getBoolean(p):
    return p.getBoolean()
def getGsnAddress(p):
    p = p.getSequence() # Not a sequence, but works the same as a 1-length sequence
    return getIpAddress(p)
def getGsnAddresses(p):
    p = p.getSequence()
    return [getIpAddress(p) for x in p.whileRemaining()]
def getPdpAddress(p):
    p = p.getSequence()
    if p.optionalTag(0): # 0 = IP Address, 1 = eTSI address
        return getIpAddress(p.getChoice())
    if p.optionalTag(1):
        return getEtsiAddress(p.getChoice())
    raise IOError("Cannot decode PDP address with address type %d" % p.getTag()[0])

def getIpAddress(p):
    if p.optionalTag(0):
        s = p.getChoice().getStringTag()
        return "%d.%d.%d.%d" % tuple(ord(x) for x in s)
    if p.optionalTag(1):
        s = p.getChoice().getStringTag()
        return "%02x%02x:%02x%02x:%02x%02x:%02x%02x:%02x%02x:%02x%02x:%02x%02x:%02x%02x" % tuple(ord(x) for x in s)
    raise IOError("Unknown IP address choice")
def getEtsiAddress(p):
    raise IOError("ETSI address decoding not implemented")


CHANGE_CONDS={1:'tariffTime', 2:'recordClosure', 12:'userLocationChange'}
def getCoCC(p):
    result = {}
    p = p.getSequenceTag()
    if p.optionalTag(2):
        result['qosNegotiated'] = p.getHex()
    if p.optionalTag(3):
        result['dataVolumeUplink'] = p.getInteger()
    if p.optionalTag(4):
        result['dataVolumeDownlink'] = p.getInteger()
    result['changeCondition'] = CHANGE_CONDS.get(p.getIntegerTag(5))
    result['changeTime'] = formatTimestamp(p.getStringTag(6))
    return result

def getCoCCs(p):
    p = p.getSequence()
    return [getCoCC(p) for x in p.whileRemaining()]

def getServiceVolume(p):
    result = {}
    p = p.getSequenceTag()
    result['id'] = p.getStringTag(0)
    result['uplinkVolume'] = p.getIntegerTag(1)
    result['downlinkVolume'] = p.getIntegerTag(2)
    return result

def getServiceVolumes(p):
    p = p.getSequenceTag(0)
    return [getServiceVolume(p) for x in p.whileRemaining()]

def getMex(p):
    result = {}
    p = p.getSequenceTag()
    result['oid'] = p.getOidTag()
    if p.optionalTag(1): # significance
        result['significance'] = p.getBoolean()
    p = p.getSetTag(2) # information
    result['information'] = getServiceVolumes(p)
    return result

def getMexs(p):
    p = p.getSet()
    return [getMex(p) for x in p.whileRemaining()]

SERVING_NODE_TYPES={0:'SGSN', 1:'PMIPSGW', 2:'GTPSGW', 3:'EPDG', 4:'HSGW', 5:'MME'}
def getServingNodeTypes(p):
    p = p.getSequence()
    return [SERVING_NODE_TYPES.get(p.getEnumeratedTag()) for x in p.whileRemaining()]

tags = {
    3:  {'name':'servedImsi', 'decoder':getString, 'formatter':formatBCD},
    4:  {'name':'servingGatewayAddress', 'decoder':getGsnAddress}, # GGSN address
    5:  {'name':'chargingId', 'decoder':getInteger},
    6:  {'name':'servingNodeAddresses', 'decoder':getGsnAddresses}, # SGSN addresses
    7:  {'name':'accessPointName', 'decoder':getString},
    8:  {'name':'pdpType', 'decoder':getString, 'formatter':formatPdpType},
    9:  {'name':'servedPdpAddress', 'decoder':getPdpAddress},
    11: {'name':'dynamicAddressFlag', 'decoder':getBoolean},
    12: {'name':'trafficVolumes', 'decoder':getCoCCs},
    13: {'name':'recordOpeningTime', 'decoder':getString, 'formatter':formatTimestamp},
    14: {'name':'duration', 'decoder':getInteger},
    15: {'name':'causeForRecordClosing', 'decoder':getInteger, 'formatter':formatCloseCause},
    17: {'name':'recordSequenceNumber', 'decoder':getInteger},
    18: {'name':'nodeId', 'decoder':getString},
    19: {'name':'managementExtensions', 'decoder':getMexs},
    20: {'name':'localSequenceNumber', 'decoder':getInteger},
    21: {'name':'apnSelectionMode', 'decoder':getEnumerated},
    22: {'name':'servedMsisdn', 'decoder':getString, 'formatter':formatMSISDN},
    23: {'name':'chargingCharacteristics', 'decoder':getHex},
    24: {'name':'chChSelectionMode', 'decoder':getEnumerated},
    27: {'name':'servingNodePlmnId', 'decoder':getString, 'formatter':formatMccMnc},
    35: {'name':'servingNodeTypes', 'decoder':getServingNodeTypes},
    38: {'name':'startTime', 'decoder':getString, 'formatter':formatTimestamp},
    39: {'name':'stopTime', 'decoder':getString, 'formatter':formatTimestamp},
    }

TAG_SWRECORD=78
TAG_RECORD_TYPE=0
# Record types
RT_SGW = 84

def parseCdr(p):
    p = p.getSetTag(TAG_SWRECORD)
    if p.getEnumeratedTag(TAG_RECORD_TYPE) != RT_SGW:
        raise IOError("Unknown record type")

    result = {}
    while p.hasRemaining():
        tagNo, cls, constructed = p.getTag()
        ti = tags[tagNo]
        format = ti.get('formatter', noformat)
        result[ti['name']] = format(ti['decoder'](p))

    return result

def parseCdrs(data):
    p = DERParser(Buffer(data))
    return [parseCdr(p) for x in p.whileRemaining()]

#!/usr/bin/env python
# encoding: utf-8
"""
generator.py

Created by Professional Services on 2012-10-15.
Copyright (c) 2012 Procera Networks Inc. All rights reserved.
"""
import sys
import os
import tempfile
import subprocess
import time
import json
import datetime
import urllib
import socket
import logging
import ftplib

############################################
######## CONFIGURATIONAL PARAMETERS ########
############################################

PSMHOST = "127.0.0.1"
PSMUSER = "admin"
PSMPASS = "pldemo00"
PSMPORT = 3994  # JSON RPC
OUTDIR = "/data/ftpaccess"
TMPDIR = "/data/ftpaccess/scdr/tmp"
COUNTER = {'in': 'incoming', 'out': 'outgoing'}
NODENAME = "r04"
JSON_TEMPLATE = '{"id": %d,"method": "object.updateByAid","params": ["session","%s",{"%s": {"op": "offset","value": -%d},"%s": {"op": "offset","value": -%d}}]}'
SUBSCRIBERS_REST_URL = "https://%s:%s@%s:8443/rest/model/objects/subscribers"
SESSIONS_REST_URL = "https://%s:%s@%s:8443/rest/model/objects/sessions"
LOG_LEVEL = logging.INFO

HEADER = ("san id", "local ip", "destination ip", "kbytes in", "kbytes out", "kbytes total", "timestamp")

# SFTP stuff
SFTP_SYNC = True
SFTP_USER = "clc"
SFTP_HOST = "10.64.208.58"
SFTP_KEY = """-----BEGIN RSA PRIVATE KEY-----
MIIEowIBAAKCAQEAwfcX+W9f5zdmYTcdSpq8m1CEJZoQR9bYkIAEIqE7lxS8J8oL
RiPjgH5vsQgjBOBKcsfkTErGPba6dLfjMP55qu73cSFH2dMAHIW8EQ9hTojpUrJk
YgmH68iZ1hJkFE+ipcuTcilOzfFPLc9ioYCATUAG2Saz2EWuDCDpaes1/eJTjiXC
9sUqjPOw4Uab5/KTSxAGjbc0kaToT35CLDYZBGt/OouCc2eCIlNwmcFEPKP8v0CO
MHI9ThgjDSpQ/TmEGCbpYtkP8jg9gJdZH1IJk8rzUWC3X7e4fTY17J2WpJCwHJSY
suhqcVxvT37i7Had/gagpdqUfpl7sBd8coXIAQIDAQABAoIBAFh44YmX4JGxdlRf
dE/kNqVNW4lfNY/fEpcOnVRCYNDv10b65JuQoSOqCD4irP57Y9npDVwzOytJHtFA
UzO0z0BFkb4bZQ+ZK9LWuUq6zjKpRmu/DQSevk2xCWJYryeIj3K6Yb3P068iI3CM
yLtLxrn1u2nvOlcqqVHE7VKvw8fSWPNOPPZNdf1nNgBgEe/0Tnw/COKP1/suq/dV
HgSAG3Eg49nmD2kHOtZaAnxjiK+YRodoHYKGi8JE4GanJKngeLATJ/eN1uZwuxn1
gCWzL/uEcLcNns4AhEtwwq6L++Tu06GCo3Z7w2nGBjtQY9o+lLscYGMCHDWAW/P2
efHvzAECgYEA9bQkcsSTPGo6nT78pYEXxwM1iX0Ic1YeSa1s4Cu9HFKIYWm1V7Rc
j1OHm9xa/Pn9ZLvt3c7zSfD2pQlEtFL0+UxiheG9ev3KDtAOhMZ0B9Z91N/vNuoT
gh6ub47wK1dHefJozRUEVQbMvI1f6hxm1WTYzrYpZc9e8yTA9EWCSGECgYEAyhfp
avHrZUcINkdDSd+pyHtt441zvIoPQUubNPWJFECIaHXYnRTzOkkW9ptH5tJI0Xq0
3bIFhV71QzyekDaK+9oCnQwpPML39kPNZkhPdIg+kSBZYOnXiq5WMGAjW2qnZp3D
lO9zjiDJ0A1q92K9c1+Pb3lejDJhK3GQzSVRI6ECgYEAqZrTOiH1nNObaGZNUhW9
ixPtBd44Uh1VRPig2lF29jEGkW+9zS/kYM+BIZbHfC84uit7tAwiJp1eNGgkc/F7
xwbyT4aXHGpJ61W1X/P5rltieuqlnxuPodd6A+oAYXqbDVPHAiIK3oKWG2XfmqRG
W/GEM5TNGMk/uslZJIVCvKECgYBoUSF+v7OXiqv1gKF+L4KvZu8ZR7nXN5iaRtGt
65Q/rPP8n+AZbWgDzRiaYRsjTaai4ukbiroI1zRY6aCbplvllupEcLOUlrtyFhuf
UXIaH/3T4dPhD7Pf9Q+uVuHJXWtdr8/2QAfw9IHX8CUn34MVW91pWEfyrEq2Jx/s
lPemIQKBgBsuxU7r7e3zNuHOwDKLe1HdxNZvOnNrEEKQEyEzH/Ea+q17s2fOz8WY
qmKiA6OPD4LNjdW8AqdKpJlfdXayHDzolEchnI+IghBH3SyHleAshHt+XxewA2fK
tk8CxhOzWGMxSPNhWItKeUxY8mQRx87ZpSQDuGIOjfOstPNQ5O7W
-----END RSA PRIVATE KEY-----"""
SFTP_DESTINATION = "/mediation/collect/SWITCHFILES/COLOCATION/"

############################################
###### END CONFIGURATIONAL PARAMETERS ######
############################################

def sftp_upload(user, host, source_file, destination_path, private_key):
    '''
    This function puts a file <source_file> at destination path
    <destination_path> at a remote host.

    This function should also be my obituary if you would please kill me.
    '''

    # Generate the sequence of commands to put the file at remote host
    batch = '\n'.join((
        "cd %s" % destination_path,
        "put %s" % source_file,
        "exit\n"
    ))

    # Write the private key to a temporary file
    key_fd, key_name = tempfile.mkstemp()
    os.write(key_fd, private_key)
    os.close(key_fd)

    # Write the batch to a temporary file
    batch_fd, batch_name = tempfile.mkstemp()
    os.write(batch_fd, batch)
    os.close(batch_fd)

    # Upload
    subprocess.check_output([
        "sftp",
        "-i", key_name,
        "-b", batch_name,
        "-o", "UserKnownHostsFile=/dev/null",
        "-o", "StrictHostKeyChecking=no",
        "-o", "LogLevel=quiet",
        "%s@%s" % (user, host)
    ])

    # Remove the temporary files
    os.unlink(key_name)
    os.unlink(batch_name)

logger = logging.getLogger("scdr.generator")


class LineConnection(object):
    def __init__(self, socket):
        self.buffer = ''
        self.socket = socket

    def send(self, line):
        self.socket.sendall(line + '\n')

    def recv(self):
        pos = self.buffer.find('\n')
        while pos < 0:
            newdata = self.socket.recv(1000)
            if len(newdata) == 0:
                raise EOFError, "connection closed by peer"
            self.buffer += newdata
            pos = self.buffer.find('\n')
        line = self.buffer[:pos]
        self.buffer = self.buffer[pos + 1:]
        return line

    def close(self):
        self.socket.close()


def get_sequence(tmpdir=TMPDIR):
    sequence = 0
    if not os.path.exists(tmpdir):
        os.makedirs(tmpdir)
    sequence_file = os.path.join(tmpdir, ".sequence")
    if os.path.exists(sequence_file):
        sequence = int(open(sequence_file, 'r').read())
        # Wrap counter
        if sequence > 9999:
            sequence = 0
    sequence += 1
    open(sequence_file, "w").write("%d" % sequence)
    return sequence


class CDRFile(file):
    def __init__(self, *args, **kwargs):
        file.__init__(self, *args, **kwargs)
        self.records = 0
        logger.info("Creating CDRFile archive: %s" % (os.path.basename(self.name)))

    def dump(self, record):
        output = ",".join([str(x) for x in record])
        logger.debug("Writing '%s'", output)
        self.write("%s\n" % output)
        self.records += 1

    def seal(self):
        self.close()
        logger.info("Sealing CDRFile archive: %s with %d records" % (os.path.basename(self.name), self.records))
        return self.records


class SimpleCDRProcessor(object):
    def __init__(self, nodename=NODENAME, psmhost=PSMHOST, psmuser=PSMUSER, psmpass=PSMPASS, psmport=PSMPORT,
                 tempdir=TMPDIR, outdir=OUTDIR, sequence=get_sequence()):
        super(SimpleCDRProcessor, self).__init__()
        # Configurational parameters
        self.nodename = nodename
        self.psmhost = psmhost
        self.psmuser = psmuser
        self.psmpass = psmpass
        self.psmport = psmport
        self.tempdir = tempdir
        self.outdir = outdir
        self.sequence = sequence

        self.tempfiles = []

        logger.info("Initiated %s" % self)

        # Statistical parameters
        self.starttime = time.time()
        self.records = 0

        logger.debug("Checking directory structure")
        try:
            if not os.path.exists(self.tempdir):
                os.makedirs(self.tempdir)
            if not os.path.exists(self.outdir):
                os.makedirs(self.outdir)
        except Exception, e:
            logger.error("Could not create directories")
            logger.exception(e)
            sys.exit(1)

        try:
            logger.info("Connecting to PSM JSON Source...")
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.connect((self.psmhost, self.psmport))
            self.lc = LineConnection(self.socket)
        except Exception, e:
            logger.error("Could not connect to PSM. Aborting execution.")
            logger.exception(e)
            sys.exit(1)

        n = datetime.datetime.now()
        self.cdrfilename = "%s%d%02d%02d%02d%02d%02d%04d.csv" % (
        self.nodename, n.year, n.month, n.day, n.hour, n.minute, n.second, self.sequence)
        self.cdrpath = os.path.join(self.tempdir, self.cdrfilename)
        if os.path.exists(self.cdrpath):
            logger.warn("File '%s' exists and will be overwritten" % self.cdrpath)

        try:
            self.cdrfile = CDRFile("%s" % self.cdrpath, "w")
        except Exception, e:
            logger.error("Could not create CDR file %s" % self.cdrpath)
            logger.exception(e)
        self.cdrfile.dump(HEADER)

    def process(self):
        logger.info("Processing started")

        self.records = 0
        records = self.__subscriber_download()
        sessions = self.__session_download()
        self.__create_cdr(records, sessions)
        self.__update_counters(records, sessions)
        self.__cleanup()
        self.cdrfile.seal()
        os.chmod(self.cdrpath, 0666)
        os.rename(self.cdrpath, os.path.join(self.outdir, self.cdrfilename))
        self.stoptime = time.time()

        logger.info("Processing finished")
        delta = self.stoptime - self.starttime
        logger.info("%d records processed in %0.2f seconds (%0.2f records/s)" % (
        self.records, delta, float(self.records) / delta))

        # Upload the generated file to the SFTP host
        if SFTP_SYNC:
            start_time = time.time()
            logger.info('Uploading records via SFTP')
            try:
                sftp_upload(
                    SFTP_USER, SFTP_HOST,
                    os.path.join(self.outdir, self.cdrfilename),
                    SFTP_DESTINATION,
                    SFTP_KEY
                )
                logger.info("File uploaded in %f seconds" % (time.time() - start_time))
            except Exception, e:
                logger.error('Unable to upload records to SFTP server: %s' % str(e))
                sys.exit(1)
            # os.unlink(os.path.join(self.outdir, self.cdrfilename))

    def __subscriber_download(self):
        logger.info("Downloading subscriber database snapshot from PSM")
        try:
            o = urllib.urlopen(SUBSCRIBERS_REST_URL % (self.psmuser, self.psmpass, self.psmhost))
            alldata = o.read()
            records = []
            for i in json.loads(alldata):
                records.append({
                    "t": time.time(),
                    "oid": i['oid'],
                    "sanId": i['sanId']
                })
                self.records += 1
            return records
        except Exception, e:
            logger.error("Problem retrieving subscriber data from the PSM. Aborting execution")
            logger.exception(e)
            logger.info("Deleting CDR file: %s" % self.cdrpath)
            os.unlink(self.cdrpath)
            sys.exit(1)


    def __session_download(self):
        logger.info("Downloading session database snapshot from PSM")
        try:
            o = urllib.urlopen(SESSIONS_REST_URL % (self.psmuser, self.psmpass, self.psmhost))
            decoded = json.loads(o.read())
            session_map = {}
            for session in decoded:
                parent = session['parentOid']
                if parent:
                    if parent not in session_map:
                        session_map[parent] = []
                    session_map[parent].append(session)
            return session_map
        except Exception, e:
            logger.error("Problem session retrieving session data from the PSM. Aborting execution")
            logger.exception(e)
            logger.info("Deleting CDR file: %s" % self.cdrpath)
            os.unlink(self.cdrpath)
            sys.exit(1)


    def __create_cdr(self, records, sessions):
        logger.info("Generating CDR files")
        for record in records:
            if record['oid'] in sessions:
                for session in sessions.get(record['oid'], []):
                    if not session['isDestinationIp']:
                        incoming = session.get(COUNTER['in'], 0) / 1024
                        outgoing = session.get(COUNTER['out'], 0) / 1024

                        outdata = (
                            record['sanId'],
                            session['sessionId'],
                            '<null>',
                            str(incoming),
                            str(outgoing),
                            str(incoming + outgoing),
                            record['t']
                        )
                        self.cdrfile.dump(outdata)
            # outdata = (str(record[0]), COUNTERS[record[4]], "0", "", str(int((record[1] + record[2]) / 1024)), "", "",
            #           str(int(record[1] / 1024)), "", str(int(record[3])))


    def __update_counters(self, records, session_map):
        logger.info("Updating subscriber counter objects in PSM")
        count = 1

        # login
        self.lc.send(json.dumps({
            "method": "system.login",
            "params": [PSMUSER, PSMPASS]
        }))
        for record in records:
            for session in session_map.get(record['oid'], []):
                if not session["isDestinationIp"]:
                    incoming = session[COUNTER['in']]
                    outgoing = session[COUNTER['out']]
                    jsoncmd = JSON_TEMPLATE % (count, session['sessionId'], COUNTER['in'], incoming, COUNTER['out'], outgoing)
                    logger.debug("Sending: " + jsoncmd)
                    self.lc.send(jsoncmd)
                    logger.debug("Received: " + self.lc.recv())
                    count += 1


    def __cleanup(self):
        logger.info("Cleaning up temporary files")


    def __str__(self):
        return "SCDR Processor - PSM Host: %s, PSM User: %s, PSM Password: *****, PSM Port: %d, Temp directory: %s, Output directory %s" % (
        self.psmhost, self.psmuser, self.psmport, self.tempdir, self.outdir)


if __name__ == '__main__':
    logging.basicConfig(format=" %(name)s - %(levelname)s - %(message)s", level=LOG_LEVEL, datefmt='%Y-%m% %H:%M:%S')
    scdr = SimpleCDRProcessor(nodename=NODENAME)
    scdr.process()

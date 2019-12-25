import os
import tempfile
import subprocess
import urllib
import packetlogic2
import datetime
import json
import ftplib
import socket
import logging
import time
import sys

############################################
######## CONFIGURATIONAL PARAMETERS ########
############################################

PSM = "127.0.0.1"
PL = ["198.18.36.5", ] # The machines to get the stats from
TIMEOUT = 10

# Path to a list of remote hosts per local host -- %s will be replaced by local host IP
STATS_PATH = "/VBBstatistics?Statistics Object/%s?Local Host/"
USER = "admin"
PASSWORD = "pldemo00"

SUBSCRIBER_TABLE = "https://%s:%s@%s:8443/rest/model/objects/subscribers?fields=oid,sanId" % (USER, PASSWORD, PSM)
SESSION_TABLE = "https://%s:%s@%s:8443/rest/model/objects/sessions?fields=sessionId,isDestinationIp,parentOid" % (USER, PASSWORD, PSM)
OUTDIR = "/data/ftpaccess/"
TMPDIR = "/data/ftpaccess/scdr/tmp"
NODENAME = "r04"
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

logger = logging.getLogger("remotecdr.generator")

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

class CDRFile(file):
    def __init__(self, *args, **kwargs):
        file.__init__(self, *args, **kwargs)
        self.records = 0

    def dump(self, record):
        output = ",".join([str(x) for x in record])
        logger.debug("Writing '%s'", output)
        self.write("%s\n" % output)
        self.records += 1

    def seal(self):
        self.close()
        logger.info("Sealing CDRFile archive: %s with %d records" % (os.path.basename(self.name), self.records))
        return self.records

def get_sequence(tmpdir=TMPDIR):
    sequence = 0
    if not os.path.exists(tmpdir):
        os.makedirs(tmpdir)
    sequence_file = os.path.join(tmpdir, ".remotesequence")
    if os.path.exists(sequence_file):
        sequence = int(open(sequence_file, 'r').read())
        # Wrap counter
        if sequence > 9999:
            sequence = 0
    sequence += 1
    file(sequence_file, "w").write("%d" % sequence)
    return sequence

def download_table(table):
    logger.info("Downloading %s" % table)
    return json.loads(urllib.urlopen(table).read())

def run(t=None):

    '''
    1. Download sessions
    2. Map sessions to their parent oid
    3. Download subscribers
    4. Inject their non-isDestinationIp (Local) sessions
    5. For each subscriber
        1. For each of their non-isDestinationIp (Local) sessions
            1. Generate entries for the children of the stats list of the path corresponding to the Session (the Remotes)
    '''

    try:
        if not os.path.exists(TMPDIR):
            os.makedirs(TMPDIR)
        if not os.path.exists(OUTDIR):
            os.makedirs(OUTDIR)
    except Exception, e:
        logger.error("Could not create directories")
        logger.exception(e)
        sys.exit(1)

    # Download subscribers
    subscribers = download_table(SUBSCRIBER_TABLE)

    # Download sessions and map to parent OID
    sessions_by_parent = {}
    s = download_table(SESSION_TABLE)

    logger.info("Indexing sessions by parent")

    for session in s:
        parent = session['parentOid']
        destination = session['isDestinationIp']
        if parent and not destination:
            if parent not in sessions_by_parent:
                sessions_by_parent[parent] = []
            sessions_by_parent[parent].append(session)

    logger.info("Mapping sessions to subscribers")
    # Map sessions to parent subscriber
    for sub in subscribers:
        oid = sub['oid']
        sub['sessions'] = sessions_by_parent.get(oid, [])

    # Ripped from the SCDR
    sequence = get_sequence()

    logger.info("Connecting to PL at %s" % PL[0])
    for pl in PL:
        try:
            packetlogic = packetlogic2.connect(pl, USER, PASSWORD, timeout=TIMEOUT)
            stats = packetlogic.Statistics()
            break
        except:
            if PL[-1] == pl:
                logger.error("Unable to connect to any PIC. Aborting")
                return
            logger.warn("Unable to connect to PIC %s; trying next" % pl)

    n = datetime.datetime.now()
    cdrfilename = "remote_%s%d%02d%02d%02d%02d%02d%04d.csv" % (NODENAME,
        n.year, n.month, n.day, n.hour, n.minute, n.second, sequence
    )
    cdrpath = os.path.join(TMPDIR, cdrfilename)

    if os.path.exists(cdrpath):
        logger.warn("File '%s' exists and will be overwritten" % self.cdrpath)

    cdrfile = CDRFile("%s" % cdrpath, "w")
    cdrfile.dump(HEADER)

    if not t:
        t = datetime.datetime.now()

        # We want to start at the last full even hour
        start_time = t - datetime.timedelta(
            hours=1, minutes=t.minute, seconds=t.second
        )

    else:
        t = datetime.datetime.strptime(t, "%Y-%m-%d %H:%M:%S")
        start_time = t

    # and end 1 hour later
    end_time = start_time + datetime.timedelta(hours=1)

    # Get the time stamp of the end time
    timestamp = int(end_time.strftime('%s'))

    # Dates need to be strings for the statistics gathering
    start_time = start_time.strftime("%Y-%m-%d %H:%M:%S")
    end_time = end_time.strftime("%Y-%m-%d %H:%M:%S")

    session_dict = {}

    logging.info("Generating records")
    for sub in subscribers:
        oid = sub['oid']
        sanid = sub['sanId']
        for session in sub['sessions']:
            ip = session['sessionId']
            try:
                remotes = stats.list(start_time, end_time, STATS_PATH % ip)
            except Exception, e:
                logger.debug("Unable to extract stats for %s: %s" % (str(sanid), str(e)))
                continue

            for remote in remotes:
                bytes_total = int(remote['values']['bytes total']) / 1024
                bytes_in = int(remote['values']['bytes in']) / 1024
                bytes_out = int(remote['values']['bytes out']) / 1024

                cdrfile.dump((
                    str(sanid),
                    '<NULL>',
                    remote['name'],
                    str(bytes_in),
                    str(bytes_out),
                    str(bytes_total),
                    timestamp
                ))

    cdrfile.seal()
    os.chmod(cdrpath, 0666)
    os.rename(cdrpath, os.path.join(OUTDIR, cdrfilename))

    # Upload the generated file to the SFTP host
    if SFTP_SYNC:
        start_time = time.time()
        logger.info('Uploading records via SFTP')
        try:
            sftp_upload(
                SFTP_USER, SFTP_HOST,
                os.path.join(OUTDIR, cdrfilename),
                SFTP_DESTINATION,
                SFTP_KEY
            )
            logger.info("File uploaded in %f seconds" % (time.time() - start_time))
        except Exception, e:
            logger.error('Unable to upload records to SFTP server: %s' % str(e))
            sys.exit(1)
        # os.unlink(os.path.join(OUTDIR, cdrfilename))

if __name__ == '__main__':
    import sys

    logging.basicConfig(format=" %(name)s - %(levelname)s - %(message)s", level=LOG_LEVEL, datefmt='%Y-%m% %H:%M:%S')

    if len(sys.argv) > 1:
        run(sys.argv[1])
    else:
        run()
            


import csv
import itertools
import sys
import telnetlib


HOST = "127.0.0.1"
PORT = "3994"

tn = telnetlib.Telnet(HOST,PORT)
tn.set_debuglevel(9)
DISCONNECT = '{"id":1, "method":"system.disconnect"}'
DELETE1 = '{"id":1, "method":"object.updateAll", "params":["subscriber", {"'
DELETE2 = '":" "}]}'
UPDATE1 = '{"id":1, "method":"object.updateByAid", "params":["subscriber", "'
UPDATE2 = '", {"'
UPDATE3 = '":"'
UPDATE4 = '"}]}'

pol = {}

with open('policy.csv') as f:
	lines = itertools.islice(f, 1, None) # skip 11 lines, simliar to [11:]
	reader = csv.reader(lines)
	for row in reader:
		POLICY = row[1]
		if not pol.has_key(POLICY):
			pol[POLICY] = 1
			DELETE_COMMAND = (DELETE1+POLICY+DELETE2)
			tn.write(DELETE_COMMAND+"\n")

		UPDATE_COMMAND = (UPDATE1+row[0]+UPDATE2+row[1]+UPDATE3+row[2]+UPDATE4)		
		tn.write(UPDATE_COMMAND+"\n")


tn.write(DISCONNECT+"\n")

print tn.read_all()
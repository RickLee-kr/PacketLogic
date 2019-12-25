#!/usr/bin/python

import socket
import random
from types import *

class Hasher:
	def __init__(self, ip1, ip2, port1, port2, proto):
		if type(ip1) is StringType:
			self.ip1 = self.ConvertIP(ip1)
		elif type(ip1) is IntType:
			self.ip1 = ip1
		elif type(ip1) is ListType:
			t = 0
			t = t | ip1[0] << 0
			t = t | ip1[1] << 8
			t = t | ip1[2] << 16
			t = t | ip1[3] << 24
			self.ip1 = t
			self.ip1 = socket.htonl(self.ip1)

		if type(ip2) is StringType:
			self.ip2 = self.ConvertIP(ip2)
		elif type(ip2) is IntType:
			self.ip2 = ip2
		elif type(ip2) is ListType:
			t = 0
			t = t | ip2[0] << 0
			t = t | ip2[1] << 8
			t = t | ip2[2] << 16
			t = t | ip2[3] << 24
			self.ip2 = t
			self.ip2 = socket.htonl(self.ip2)

		self.port1 = socket.htons(port1)
		self.port2 = socket.htons(port2)
		self.proto = proto

	def ConvertIP(self, ip):
		t = ip.split('.')
		t = [int(i) & 0xff for i in t]
		res = 0
		res = res | t[0] << 0
		res = res | t[1] << 8
		res = res | t[2] << 16
		res = res | t[3] << 24
		return res

	def HashFunction(self):
#		print "%x ^ %x = %x" % (self.ip1, self.ip2, self.ip1 ^ self.ip2)
		h = self.proto ^ (self.port1 ^ self.port2) ^ (self.ip1 ^ self.ip2)
		return h

def PrintDistribution(arr, radix, head, prefix = ""):
	seg = radix / 10
	res = []
	for i in range(11):
		res.append(0)
	for n in arr:
		if n > radix:
			res[10] = res[10] + 1
		else:
			i = n / seg
			res[i] = res[i] + 1
	print "%s" % head
	for i in range(10):
		print "%sEntries with %d-%d results:\t\t%d" % (prefix, seg * i, seg * (i + 1), res[i])
	print "%sEntries with more than %d results:\t%d" % (prefix, radix, res[10])

random.seed()

print "Creating large array"
arr = []
for i in range(1024 * 1024):
	arr.append(0)

print "Starting random sequence"
for i in range(1024 * 1024 * 10):
	if i % (1024 * 100) == 0:
		print "\tReached sequence %d" % i

	rr1 = random.randint(192, 255)
	rr2 = random.randint(0, 255)
	rr3 = random.randint(0, 255)
	rr4 = random.randint(0, 255)

	lr1 = random.randint(0, 255)
	lp = random.randint(1024, 1024 * 64)
	rp = random.randint(1024, 1024 * 64)

	hasher = Hasher([213, 168, 0, lr1], [213, 168, 3, rr4], lp, rp, 7)
	#hasher = Hasher([0, 0, 0, 0], [0, 0, 0, 0], lp, rp, 7)
	h = hasher.HashFunction()
	j = h % (1024 * 1024)
	arr[j] = arr[j] + 1

PrintDistribution(arr, 100, 'Results:', '\t')


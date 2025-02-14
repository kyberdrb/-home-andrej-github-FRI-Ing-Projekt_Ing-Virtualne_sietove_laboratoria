#! /usr/bin/env python

print "*********************************************************************"
print "Cisco IOU License Generator - Kal 2011, python port of 2006 C version"

import os
import socket
import hashlib
import struct

# get the host id and host name to calculate the hostkey
hostid=os.popen("hostid").read().strip()
hostname = socket.gethostname()
ioukey=int(hostid,16)
for x in hostname:
  ioukey = ioukey + ord(x)

print "hostid=" + hostid +", hostname="+ hostname + ", ioukey=" + hex(ioukey)[2:]

# create the license using md5sum
iouPad1='\x4B\x58\x21\x81\x56\x7B\x0D\xF3\x21\x43\x9B\x7E\xAC\x1D\xE6\x8A'
iouPad2='\x80' + 39*'\0'
md5input=iouPad1 + iouPad2 + struct.pack('!i', ioukey) + iouPad1
iouLicense=hashlib.md5(md5input).hexdigest()[:16]

with open("/opt/unetlab/addons/iol/bin/iourc", 'w') as iourc:
    iourc.write("[license]\n")
    iourc.write(hostname + " = " + iouLicense + ";\n")

with open("/etc/hosts", 'a') as hosts:
    hosts.write("127.0.0.127 xml.cisco.com\n")

print "\nA 'iourc' license file has been generated in /opt/unetlab/addons/iol/bin/"
print "[license]\n" + hostname + " = " + iouLicense + ";\n"
print "The Cisco Phone Home feature has been disabled by appending the line below in hosts file:"
print "127.0.0.127 xml.cisco.com\n"


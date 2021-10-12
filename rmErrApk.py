#!/usr/bin/python
# -*- coding: utf-8 -*- 

import os, sys, time, threading, shlex
import urllib, urllib2
from optparse import OptionParser
#from com.android.monkeyrunner import MonkeyRunner, MonkeyDevice
from xml.dom import minidom
from os.path import join, isdir, isfile, getsize
from subprocess import Popen, PIPE
import random

APPDUMP = 'exp5_checkZip.txt'

def myExit(code):
    print '[Main] Start exiting...'
    sys.exit(code)

def flush():
    sys.stdout.flush()


"""
==============
main entry
==============
"""
# parse parameters
usage = "usage: python %prog -f listfile"
parser = OptionParser(usage=usage)
parser.add_option('-f', '--listfile', action='store', type='string', dest='listfile',
        help='The app dump file.')
(options, args) = parser.parse_args()
if not options.listfile:
    parser.error('-f (listfile) is mandatory')
APPDUMP = options.listfile


# read app list
applist = []
print '[Main] Read app list...'
flush()
f = open(APPDUMP, 'r')
for line in f:
    app = line.rstrip()
    applist.append(app)
if f:
    f.close()

print len(applist)


# http://stackoverflow.com/a/415525/197165
curtime = time.strftime("%Y-%m-%d %H:%M:%S")
print 'Current Time: ', curtime
flush()


# loop app list
i = 0
for sha in applist:
    i = i + 1
    cmd = 'rm %s' % sha
    os.system(cmd)  # will hold on here
    print '[%d] %s' % (i, cmd)
    flush()


curtime = time.strftime("%Y-%m-%d %H:%M:%S")
print 'Current Time: ', curtime
flush()

# exit
myExit(0)

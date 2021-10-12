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

APPDUMP = 'repackaging_15297.txt'

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
applist = {}
print '[Main] Read SHA256 list...'
flush()
f = open(APPDUMP, 'r')
for line in f:
    sha = line.rstrip()  #no matter \r or \n
    applist[sha] = sha   #TODO pkg is empty here
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
    pkg = applist[sha]  #TODO actually sha here

    appname = '%s.apk' % pkg
    if os.path.exists(appname):
        print '[%d] Skip App: %s' % (i, pkg)
        flush()
        continue

    print '[%d] Fetech App: %s' % (i, pkg)
    flush()
    cmd = 'curl -o %s.apk --remote-header-name -G -d apikey=6c8ab02333d02cdb0e37db3235eb36cf56a02d822aaba543be4684c004d8698c -d sha256=%s https://androzoo.uni.lu/api/download' % (pkg, sha)
    os.system(cmd)  # will hold on here


curtime = time.strftime("%Y-%m-%d %H:%M:%S")
print 'Current Time: ', curtime
flush()

# exit
myExit(0)

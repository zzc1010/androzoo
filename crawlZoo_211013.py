#!/usr/bin/python
# -*- coding: utf-8 -*- 
# download app from androzoo
import os, sys, time, threading, shlex
import urllib, urllib2
from optparse import OptionParser
#from com.android.monkeyrunner import MonkeyRunner, MonkeyDevice
from xml.dom import minidom
from os.path import join, isdir, isfile, getsize
from subprocess import Popen, PIPE
import random


outputDir = '../1013Testapps'

def mkdir(path):
    folder = os.path.exists(path)
    if not folder:  # 判断是否存在文件夹如果不存在则创建为文件夹
        os.makedirs(path)  # makedirs 创建文件时如果路径不存在会创建这个路径
        print("---  new folder... %s ---" % path)

#packagename, sha256
def myExit(code):
    print '[Main] Start exiting...'
    sys.exit(code)

def flush():
    sys.stdout.flush()


# parse parameters
def startCrawling(inputPath, cat):
    mkdir(outputDir+"/"+cat)


    # read app list
    applist = {}
    print '[Main] Read app list...'+cat
    flush()
    f = open(inputPath, 'r')
    for line in f:
        app = line.rstrip('\n')
        splits = app.split(',')
        pkg = splits[0]
        sha = splits[1]
        applist[sha] = pkg
    if f:
        f.close()

    print len(applist)


    # http://stackoverflow.com/a/415525/197165
    curtime = time.strftime("%Y-%m-%d %H:%M:%S")
    print 'Current Time: ', curtime, cat
    flush()


    # loop app list
    i = 0
    for sha in applist:
        i = i + 1
        pkg = applist[sha]

        appname = '%s.apk' % pkg
        if os.path.exists(appname):
            print '[%d] Skip App: %s' % (i, pkg), cat
            flush()
            continue

        print '[%d] Fetech App: %s' % (i, pkg), cat
        flush()
        cmd = 'curl -o %s.apk --remote-header-name -G -d apikey=6c8ab02333d02cdb0e37db3235eb36cf56a02d822aaba543be4684c004d8698c -d sha256=%s https://androzoo.uni.lu/api/download' % (outputDir+"/"+cat+"/"+pkg, sha)
        os.system(cmd)  # will hold on here


    curtime = time.strftime("%Y-%m-%d %H:%M:%S")
    print 'Current Time: ', curtime, cat
    flush()

"""
==============
main entry
==============
"""
usage = "usage: python %prog -f listfile"
parser = OptionParser(usage=usage)
parser.add_option('-f', '--listfile', action='store', type='string', dest='listfile',
        help='The app dump file.')
(options, args) = parser.parse_args()
if not options.listfile:
    parser.error('-f (listfile) is mandatory')
cat = options.listfile

#cat = "LIBRARIES_AND_DEMO"
APPDUMP = 'output/'+cat+'.csv'
startCrawling(APPDUMP, cat)
myExit(0
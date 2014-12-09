#!/usr/bin/env python

import os
import sys
import time
import random
import requests
import argparse

parser = argparse.ArgumentParser(description="Kepps a webapp up.")
parser.add_argument("--pidfile", action="store", 
		    default="/var/run/webapp-up-keeper.pid", help="where to save the pidfile.")
parser.add_argument("--logfile", action="store", help="set the log file",
		    default="/var/log/webapp-up-keeper.log")

__debug = False

if os.environ.get("DEBUG") == "TRUE" :
	__debug = True
	print "We will debug..."

## If not debugging, fork to background.
pid = None
if __debug :
	pid = 0 
else :
	pid = os.fork()
	## let's just prevent bad shit from happenind
	if  pid == -1 :
		print "COULD NOT FORK TO BACKGROUND, THIS IS NOT SUPPOSED TO HAPPEN."
		sys.exit(1)
		

# program is forked, we can exit.
if pid != 0 :
	sys.exit(0)

## We now write the pidfile...
args = parser.parse_args()
try :
	with open(args.pidfile, "w") as pidfile :
		pidfile.write("%d\n" % os.getpid())
except :
	print "Could not open pidfile %s" % args.pidfile


## okay we're daemonized, let's behave properly...
if not __debug :
	os.chdir("/")
	sys.stdin.close()
	sys.stdout.close()
	sys.stderr.close()

	sys.stdin = open("/dev/null", "r")
	sys.stdout = open(args.logfile, "a+")
	sys.stderr = sys.stdout

## Okay now we're a decend deamon, let's do our job...

target = os.environ.get("WEB_APP") 
if not target :
	print "$WEB_APP environment variable not set, exiting..." ;
	sys.exit(0)


response = None
while True :
	try :
		if __debug :
			print "sleeping..."
		time.sleep(30 + random.randrange(0, 30))
		response = requests.get(target) ;
	except :
		print "Unable to perform the request... (%s)" % time.ctime()
		continue

	if __debug :
		print "%s: %s (%s)" % (time.ctime(), response.status_code, response.reason)
	if response.status_code != requests.codes.ok :
		print "HTTP server at %s reponded with status code %d (%s)" % (target, response.status_code, response.reason)


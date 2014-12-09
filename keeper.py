#!/usr/bin/env python

import os
import sys
import time
import random
import requests

__debug = False

if os.environ.get("DEBUG") == "TRUE" :
	__debug = True
	print "We will debug..."

pid = None
if __debug :
	pid = 0 
else :
	pid = os.fork()

# let's fork...
if pid != 0 :
	sys.exit(0)


## okay we're daemonized, let's behave properly...
if not __debug :
	os.chdir("/")
	sys.stdin.close()
	sys.stdout.close()
	sys.stderr.close()

	sys.stdout = open("/var/log/heroku-up-keeper.log", "a+")
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


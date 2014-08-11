#!/usr/bin/python
# to get a list of dir and stop when you see smali

import os, subprocess, time, sys
y = '/home/ameya/Documents/Privacy_Research/'
y1 = '/home/ameya/Documents/Privacy_Research/Talking_Tom/smali/0017C8799506E6133B30401274B39940/res'
name = "smali"
print len( [f for f in os.listdir(y1) if os.path.isdir(os.path.join(y1,f))])
for path, dirs,files in os.walk(y):
	if name in dirs:
		print "Yes"
		print os.path.join(path,name)
		os.chdir(os.path.join(path,name))
		subprocess.call(['ls'])

#!/usr/bin/env python
# encoding: utf-8
"""
reloader.py

Convenience function to kick apache whenever any project files are modified. Sudo this to get
access to apache init script.

Created by mikepk on 2009-06-30.
Copyright (c) 2009 Michael Kowalchik. All rights reserved.
"""
import os
import sys
import getopt
import re

import time

help_message = '''
Simple reloader script to check whether code has been modified and reloads
the application server if so

help ...  this message
path ...  the root path to check
'''


class Usage(Exception):
    def __init__(self, msg):
        self.msg = msg


mods = {}


def init(path,list):
    gen = os.walk(path)

    allfiles = []
    #init time changes
    for dirpath,dirnames,names in gen:
        include = re.compile("(\.py|\.template|\.wsgi)$", re.IGNORECASE)          
        dontinclude = re.compile("^\.\_|\.template\.py$", re.IGNORECASE)          
        list = filter(include.search, names)
        list = filter(lambda x: not dontinclude.search(x), list)

        for name in list:
            #print name
            mods[dirpath+'/'+name] = os.path.getmtime(dirpath+'/'+name)
            allfiles.append(dirpath+'/'+name)
    return allfiles
  

def test_modification_time(list):
    while 1:
        for name in list:
            if mods[name] != os.path.getmtime(name):
                print "Project changed, "+name+" modified. Restarting web server"
                return 0
        time.sleep(2)
    

def main(argv=None):
    if argv is None:
        argv = sys.argv
    try:
        try:
            opts, args = getopt.getopt(argv[1:], "pho:v", ["help", "output=", "path="])
        except getopt.error, msg:
            raise Usage(msg)
    
        # option processing
        for option, value in opts:
            if option == "-v":
                verbose = True
            if option in ("-h", "--help"):
                raise Usage(help_message)
            if option in ("-o", "--output"):
                output = value
            if option in ("-p", "--path"):
                path = value

        allfiles = []
        allfiles=init(path,allfiles)

        while 1:
            if test_modification_time(allfiles):
                pass
            else:
                print "Restarting Apache2..."
                os.system('/etc/init.d/apache2 reload')
                init(path,allfiles)
        
    
    except Usage, err:
        print >> sys.stderr, sys.argv[0].split("/")[-1] + ": " + str(err.msg)
        print >> sys.stderr, "\t for help use --help"
        return 2


if __name__ == "__main__":
    sys.exit(main())

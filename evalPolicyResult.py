#!/usr/bin/python

import json, sys

with open('result.json') as json_file:  
    data = json.load(json_file)
    failed_checks = {k: v for (k, v) in data[0].iteritems() if v == False}
    if len(failed_checks) > 0:
        print "Policy Check Failures Detected!"
        print "Failed policy checks:"
        for (k, v) in failed_checks.iteritems():
            print "{}".format(k)
        sys.exit(-1)
    else:
        print "All Policy Checks Succeeded!"

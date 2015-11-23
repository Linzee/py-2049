#!/usr/bin/env python
# -*- coding: utf-8 -*-

DATA_PATH = 'delays.json'

import sys
from optparse import OptionParser

parser = OptionParser()
parser.add_option("-t", "--train",
                  dest="train",
                  help="Search for train or group of trains by name")
parser.add_option("-p", "--probability",
                  dest="probability", action="store_true", default=False,
                  help="Calculate probability to reach destination")
parser.add_option("-d", "--delays-file",
                  dest="path", default=DATA_PATH, metavar="FILE",
                  help="Change path to delays file")
parser.add_option("-s", "--show",
                  dest="show", action="store_true", default=False,
                  help="Only show graph (else they are stored in file)")

options, optionsValues = parser.parse_args()

# fix console encoding
for option, value in vars(options).iteritems():
    if isinstance(value, basestring):
        setattr(options, option, value.decode(sys.getfilesystemencoding()))
for i in range(0, len(optionsValues)):
    optionsValues[i] = optionsValues[i].decode(sys.getfilesystemencoding())

DATA_PATH = options.path

if not options.probability:
    from stats import stats
    stats(DATA_PATH, options)
else:
    from probability import probability
    probability(DATA_PATH, optionsValues)
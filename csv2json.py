#! /usr/bin/env python

"""
Script for converting a CSV file into a set of JSON data files which can be
served from any webserver.
"""

import os
import sys
import csv
import json

def parse_csv(filename, pk=None):
    res = {}
    reader = csv.DictReader(open(filename, 'rb'))
    for linum,line in enumerate(reader):
        uid = line.get(pk) or linum
        res[uid] = line

    return res

def output(items, outputdir):
    for k,struct in items.items():
        filename = '{0}.json'.format(k)
        with open(os.path.join(outputdir, filename), 'w') as f:
            f.write(json.dumps(struct))

def main(args=None, parse_csv=parse_csv, output=output,
         hooks=None):
    from optparse import OptionParser
    usage = "Usage: %prog source.csv primarykey /path/to/outputdir"
    parser = OptionParser(usage)

    args = args or sys.argv[1:]
    options, arguments = parser.parse_args(args=args)
    
    csvfilename = arguments[0]
    pk = arguments[1]
    outputdir = arguments[2]

    # parse input
    items = parse_csv(csvfilename, pk)

    # hooks
    hooks = hooks or []
    for hook in hooks:
        hook(items)

    # process output
    output(items, outputdir)
        

if __name__ == '__main__':
    main()

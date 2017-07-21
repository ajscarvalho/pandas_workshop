# -*- coding: utf-8 -*-

#relative paths
import os, sys, inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)

libdir = os.path.join(parentdir, 'lib')
datadir = os.path.join(parentdir, 'data')

sys.path.insert(0, libdir)


#parse arguments
import argparse

parser = argparse.ArgumentParser('''creates a random log file to start the workshop''')
parser.add_argument('-r', '--rubbish', metavar='Rubbish', type=int, default=90   , required=False,
    help='percentage of rubbish in log file (default: 90)'
)
parser.add_argument('-s', '--size',    metavar='Size',    type=str, default='10M', required=False,
    help='aproximate size of data set (1M = 1 Million lines) [1G]'
)

arguments = vars(parser.parse_args()) # vars turns return into dict
print(arguments)

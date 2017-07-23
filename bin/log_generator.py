# -*- coding: utf-8 -*-

#relative paths
import os, sys, inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)

libdir = os.path.join(parentdir, 'lib')
dwhdir = os.path.join(parentdir, 'dwh')

sys.path.insert(0, libdir)


#parse arguments
import argparse

parser = argparse.ArgumentParser('''creates a random log file to start the workshop''')
parser.add_argument('-r', '--rubbish', metavar='Rubbish', type=int, default=90   , required=False,
    help='percentage of rubbish in log file (default: 90)'
)
parser.add_argument('-s', '--size',    metavar='Size',    type=str, default='10M', required=False,
    help='aproximate size of data set (1M = 1 Million lines) [10M]'
)

arguments = vars(parser.parse_args()) # vars turns return into dict
#print(arguments)


# getting arguments
def get_log_file_size(size):
    multiplier = 1
    size = size.upper()
    if   size[-1] == 'K': multiplier = 1000
    elif size[-1] == 'M': multiplier = 1000000
    elif size[-1] == 'G': multiplier = 1000000000

    if multiplier > 1: size = size[:-1]
    size = int(size)
    return size * multiplier


rubbish = float(arguments.get('rubbish'))/100
size = get_log_file_size(arguments.get('size'))



# generate log file

from data.generators.logfile import LogFileGenerator

generator = LogFileGenerator(size, rubbish)
filename = os.path.join(dwhdir, 'activity')
generator.run()

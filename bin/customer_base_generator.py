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

parser = argparse.ArgumentParser('''creates a list of random ids to identify customers, required to start the workshop''')
parser.add_argument('-s', '--size',    metavar='Size',    type=str, default='10K', required=False,
    help='size of data set (1K = 1 Thousand lines) [10K]'
)

arguments = vars(parser.parse_args()) # vars turns return into dict
#print(arguments)


# getting arguments
from helper.numbers import human_readable_int_to_machine
def get_data_size(size):
    size = size.upper()
    multiplier = 1
    if   size[-1] == 'K': multiplier = 1000
    elif size[-1] == 'M': multiplier = 1000000
    elif size[-1] == 'G': multiplier = 1000000000

    if multiplier > 1: size = size[:-1]
    size = int(size)
    return size * multiplier


size = human_readable_int_to_machine(arguments.get('size'))

print ("Going to generate {} customers".format(size))



# generate customers file

from data.generators.customer_base import CustomerGenerator

filename = os.path.join(dwhdir, 'customers')
generator = CustomerGenerator(size)
generator.run(filename)

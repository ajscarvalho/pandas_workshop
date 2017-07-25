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

parser = argparse.ArgumentParser('''creates a list of random programs for known channels, required to start the workshop''')
parser.add_argument('-s', '--size',    metavar='Size',    type=str, default='10K', required=False,
    help='size of data set (1K = 1 Thousand lines) [10K]'
)

arguments = vars(parser.parse_args()) # vars turns return into dict
#print(arguments)


# getting arguments
from helper.numbers import human_readable_int_to_machine

size = human_readable_int_to_machine(arguments.get('size'))
print ("Going to generate {} programs".format(size))



from helper.words import get_words
from data.generators.epg_programs import ProgramsGenerator
#from data.access.tv_channels import TvChannelsCsvDao <- in events



words = get_words(parentdir)

filename = os.path.join(dwhdir, 'programs')
#channelsDao = TvChannelsCsvDao().load()
generator = ProgramsGenerator(words, size) #channelsDao, <- in events
generator.run(filename)

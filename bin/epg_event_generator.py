# -*- coding: utf-8 -*-

#relative paths
import os, sys, inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)

libdir = os.path.join(parentdir, 'lib')
dwhdir = os.path.join(parentdir, 'dwh')

sys.path.insert(0, libdir)

from datetime import datetime
startTS = datetime.now()

#parse arguments
import argparse

parser = argparse.ArgumentParser('''creates a list of random events for known channels and programs, required to start the workshop''')
parser.add_argument('-s', '--size',    metavar='Size',    type=int, default=10, required=False,
    help='number of days in EPG [10] (max: 29)'
)

arguments = vars(parser.parse_args()) # vars turns return into dict
#print(arguments)


# getting arguments

days = arguments.get('size')
print ("Going to generate events in every channel for {} days".format(days))



from data.generators.epg_events import EventsGenerator
from data.access.tv_channels    import TvChannelsCsvDao
from data.access.epg_programs   import EpgProgramsCsvDao


filename = os.path.join(dwhdir, 'events')
channelsDao = TvChannelsCsvDao(dwhdir) .load()
programsDao = EpgProgramsCsvDao(dwhdir).load()
generator = EventsGenerator(channelsDao, programsDao, days)
generator.run(filename)

print("Process took {:6.3f} seconds".format( (datetime.now() - startTS).total_seconds()  ))
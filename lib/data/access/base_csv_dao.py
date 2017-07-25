# -*- coding: utf-8 -*-

import pandas as pd
import os



class BaseCsvDao(object):

    def __init__(self, path):
        self.dataPath = path
        self.dataFile = '<undefined>'
        self.data = None


    def load(self):
        filename = os.path.join(self.dataPath, self.dataFile + '.csv')
        
        try:
            self.data = pd.load_csv(filename, sep=',', encoding='utf-8')
        except:
            print ("Channels File not found: ", filename)

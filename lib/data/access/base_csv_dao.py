# -*- coding: utf-8 -*-

import pandas as pd
import os



class BaseCsvDao(object):

    def __init__(self, path):
        self.dataPath = path
        self.dataFile = '<undefined>'
        self.data = None
        self.columnNames = None
        self.columnDataTypes = None
        self.nanReplacement = '' # can be dict from column to value


    def load(self):
        filename = os.path.join(self.dataPath, self.dataFile + '.csv')
        
        if self.columnNames is None:
            header = 'infer'
        else:
            header = None

        try:
            self.data = pd.read_csv(filename, sep=',', encoding='utf-8', header=header, names=self.columnNames,
                dtype=self.columnDataTypes)

            self.data.fillna(self.nanReplacement, inplace=True)
            print (self.data.head(1))
        except:
            print ("File not found: ", filename)

        return self




    def __len__(self):
        if self.data is None: return 0
        return self.data.shape[0] # assume dataframe and len is row count


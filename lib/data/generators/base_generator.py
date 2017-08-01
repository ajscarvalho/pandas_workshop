# -*- coding: utf-8 -*-

import io


class BaseGenerator(object):
    def __init__(self, size):
        self.size = size
        self.BLOCK_SIZE = 1000
        self.FILE_EXT = ".gen"
        self.linesWritten = 0


    def run(self, filename):
        filename = filename + self.FILE_EXT
        self.generatedLines = 0
        with io.open(filename, "w+", encoding='utf-8') as f:
            self.write_lines(f)


    def write_lines(self, f):
        lines = self.get_initial_lines()
        if lines: self.write_lines_to_file(f, lines)
        
        while self.linesWritten < self.size:
            lines = self.get_lines()
            self.write_lines_to_file(f, lines)
            self.linesWritten += len(lines)
            print("Wrote {:7d} lines".format(self.linesWritten))

            
    def write_lines_to_file(self, f, lines):
        content = '\n'.join(lines) + '\n'
        f.write(content)
        

    def get_lines(self):
        lines = []

        try:
            for i in range(self.BLOCK_SIZE):
                lines.append(self.get_line())           # throws StopIteration when no more lines, and ...
                if self.terminate_lines_block(): break
        
        except StopIteration:                           # returns lines 
            print ("stopping iteration at {} of {}".format(self.linesWritten, self.size))
            self.size = self.linesWritten                    # reducing size to number of lines written will make it stop

        return lines


    # meant to be overriden
    def terminate_lines_block(self): return False
    def get_initial_lines(self):     return []
    def get_line(self):              pass

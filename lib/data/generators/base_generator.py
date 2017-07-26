# -*- coding: utf-8 -*-

import io


class BaseGenerator(object):
    def __init__(self, size):
        self.size = size
        self.BLOCK_SIZE = 1000
        self.FILE_EXT = ".gen"


    def run(self, filename):
        filename = filename + self.FILE_EXT
        self.generatedLines = 0
        with io.open(filename, "w+", encoding='utf-8') as f:
            self.write_lines(f)


    def write_lines(self, f):
        linesWritten = 0
        while linesWritten < self.size:
            lines = self.get_lines()
            content = '\n'.join(lines) + '\n'
            f.write(content)
            linesWritten += len(lines)
            print("Wrote {:7d} lines".format(linesWritten))


    def get_lines(self):
        lines = self.get_initial_lines()
        for i in range(self.BLOCK_SIZE):
            lines.append(self.get_line())
            if self.terminate_lines_block(): break

        return lines

    def terminate_lines_block(self): return False

    def get_line(self):
        pass

    def get_initial_lines(self): return []

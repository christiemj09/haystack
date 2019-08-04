#!/usr/bin/env python
"""
Give file coordinates for occurrences of a string in a set of files.
"""

import csv
import os
import sys

from config import from_config


def occurrence_indices(cell, string):
    yield from occurrence_indices_aux(cell, string, 0)


def occurrence_indices_aux(cell, string, pos):
    index = cell.find(string)
    if index != -1:
        yield pos + index
        length_from_pos = index + len(string)
        remaining_cell = cell[length_from_pos:]
        yield from occurrence_indices_aux(remaining_cell, string, pos + length_from_pos)


class FileCoordinates(object):
    
    def __init__(self, filename):
        self.filename = filename
    
    def of(self, string):
        with open(self.filename, 'r') as file_in:
            reader = csv.reader(file_in)
            for row_offset, row in enumerate(reader):
                for column_offset, cell in enumerate(row):
                    for cell_offset in occurrence_indices(cell, string):
                        yield row_offset, column_offset, cell_offset
    
    def row_at(self, row_offset):
        with open(self.filename, 'r') as file_in:
            reader = csv.reader(file_in)
            for i, row in enumerate(reader):
                if i == row_offset:
                    return row


def main(filenames, output_filename, string):
    with open(output_filename, 'w') as file_out:
        writer = csv.writer(file_out)
        writer.writerow(['file_id', 'row_offset', 'column_offset', 'cell_offset'])
        for file_id, filename in enumerate(filenames):
            file_coordinates = FileCoordinates(filename)
            for row_offset, column_offset, cell_offset in file_coordinates.of(string):
                writer.writerow([file_id, row_offset, column_offset, cell_offset])


if __name__ == '__main__':
    script, config = sys.argv
    from_config(main)(config)

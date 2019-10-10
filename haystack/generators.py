"""
Field address generators.
"""

import csv
import json


class AddressGenerator(object):
    """Generates field addresses for values in a file."""
    
    def __init__(self, filename):
        self.filename = filename
    
    def address_base(self):
        return '{file_type}://{file_name}'.format(
            file_type = self.file_type,
            file_name = self.filename
        )
    
    def address(self, *args, **kwargs):
        return '/'.join([self.address_base(), self.file_type_address(*args, **kwargs)])
    
    def iterfields(self):
        """Iterate over fields in a file."""
        with open(self.filename, 'r') as file_in:
            for address_input, value in self.iterfields_for(file_in):
                yield self.address(**address_input), value


class CSVAddressGenerator(AddressGenerator):
    """Generates field addresses for values in a CSV file."""
    
    file_type = 'csv'
    
    def file_type_address(self, row_offset, col_offset):
        return '/'.join([str(row_offset), str(col_offset)])
    
    def iterfields_for(self, file_in):
        """Iterate over fields in a CSV file."""
        reader = csv.reader(file_in)
        for row_offset, row in enumerate(reader):
            for col_offset, value in enumerate(row):
                yield {'row_offset': row_offset, 'col_offset': col_offset}, value


class JSONLinesAddressGenerator(AddressGenerator):
    """Generates field addresses for values in a file containing JSON records on each line."""
    
    file_type = 'jsonl'
    
    def file_type_address(self, line_offset, path):
        path_string = ','.join('"{k}"'.format(k=k) if type(k) is str else str(k) for k in path)
        return '/'.join([str(line_offset), path_string])
    
    def value_paths(self, doc):
        for path, value in self.value_paths_aux([], doc):
            yield path, value
    
    def value_paths_aux(self, cur_path, doc):
        if type(doc) is dict:
            for key, next_doc in doc.items():
                next_path = list(cur_path)
                next_path.append(key)
                for path, value in self.value_paths_aux(next_path, next_doc):
                    yield path, value
        elif type(doc) is list:
            for key, next_doc in enumerate(doc):
                next_path = list(cur_path)
                next_path.append(key)
                for path, value in self.value_paths_aux(next_path, next_doc):
                    yield path, value
        else:
            yield cur_path, doc
    
    def iterfields_for(self, file_in):
        """Iterate over fields in a JSON file."""
        for line_offset, line in enumerate(file_in):
            doc = json.loads(line)
            for path, value in self.value_paths(doc):
                yield {'line_offset': line_offset, 'path': path}, value

    
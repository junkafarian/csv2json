csv2json
========

A utility for converting CSV datasets into individual .json files which can be
used to serve client-side applications without needing to load the full dataset.


Usage
=====

The library provides a very simple framework for reading a .csv file and
outputting individual .json files for each row of the dataset. The basic usage
is::

        python csv2json.py input.csv primary_column_key /path/to/output/dir/


Advanced Usage
==============

The library can be easily extended to process the data before it is saved to the
output format. For example, given the file ``custom.py`` in the same directory::

    def cleaner(items):
        """ remove any blank columns from the JSON structure
        """
        for struct in items.values():
            for k,v in struct.items():
                if k == '':
                    del struct[k]

    if __name__ == '__main__':
        from csv2json import main
        hooks = [
            cleaner,
            ]
        main(hooks=hooks)

This can then be run from the command line like so::

        python custom.py input.csv primary_column_key /path/to/output/dir/


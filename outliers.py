#!/usr/bin/env python
from subprocess import call
import os
import sys

def main(caipy_output_file):
    extract_possible_coding_denovo_genes(caipy_output_file)

def extract_possible_coding_denovo_genes(caipy_output_file):
    """ Function uses output file of the script cai.py and extracts sequences with CAI value larger than 0.75. """

    output = create_file()
    with open(output, "w") as output:
        with open(caipy_output_file) as open_file:
            for line in open_file:
                line_content = line.split("\t")
                if float(line_content[1]) >= 0.75:
                    output.write(line_content[0] + '\t' + line_content[1] + '\n')



def create_file():
    """ Creates files in the current working directory. Files need to be named during the process.
     Function returns full path to the new file."""

    name = raw_input("Enter name for output file (outliers_output.txt would be nice):")
    call(["touch", name])
    path = os.getcwd()
    output_file = path + "/" + name
    return output_file

if __name__ == "__main__":
    function = 'main'
    doc = locals()[function].__doc__
    if len(sys.argv) != 2:
        print 'Bad number of arguments: {0}'.format(len(sys.argv) - 1)
        print 'Module %s%s\nFunction %s \n %s' %(__file__, __doc__, function, doc )
        sys.exit(1)
    main(*sys.argv[1:])

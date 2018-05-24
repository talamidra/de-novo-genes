#!/usr/bin/env python

# customized for my "file naming system"

import sys
from Bio.SeqUtils.CodonUsage import CodonAdaptationIndex as CAI
from Bio import SeqIO
from subprocess import call
import os

def main(standard, denovo, nongenes):
    """ Calculates CAI values for each of our putative de novo genes. Uses class
    CodonAdaptationIndex from BioPython.SeqUtils.CodonUsage which source code can be
    seen here: http://biopython.org/DIST/docs/api/Bio.SeqUtils.CodonUsage-pysrc.html#CodonAdaptationIndex
    Arguments:
    standard = fasta file with highly expressed gene used to generate index and as a positive control,
    denovo = fasta file with putative de novo gene sequences,
    nongenes = fasta file with noncoding intergenic sequences (negative control)."""

    CAI_instance = CAI()

    index_generation(standard, CAI_instance)

    CAI_calculation(standard, CAI_instance)
    CAI_calculation(denovo, CAI_instance)
    CAI_calculation(nongenes, CAI_instance)


def index_generation(standard, instance):
    """ Generates index (for each codon from highly expressed genes) used for
    calculating cai values, otherwise SharpIndex would be used."""

    instance.generate_index(standard)

    print "Your index is set."


def CAI_calculation(input_file, instance):
    """ Calculates CAI for genes in input file and writes the result in the output file.
    Arguments:
    input_file = fasta file with genes which CAI I need to know: standard/denovo/nongenes
    Names of the files should end with name of the gene group (standard.fasta, denovo.fasta, nongenes.fasta),
    otherwise the conditions within this function do not work.
    instance = instance for CodonAdaptationIndex"""

    output_file = create_file()

    with open(input_file, "r") as in_file:
        with open(output_file, "w") as out_file:
            if input_file.endswith("denovo.fasta") or input_file.endswith("standard.fasta"):
                for record in SeqIO.parse(in_file, "fasta"):
                    gene_id = record.id
                    sequence = str(record.seq)
                    if len(sequence)%3 == 0 and len(sequence) >= 9:
                        CAI_value = str(instance.cai_for_gene(sequence))
                        out_file.write(gene_id + "\t" + CAI_value + "\n")
                    else:
                        raise ValueError(gene_id + ":This sequence is not a multiple of 3 or is too short.")


            elif input_file.endswith("nongenes.fasta"):
                for record in SeqIO.parse(in_file, "fasta"):
                    gene_id = record.id
                    sequence = str(record.seq)
                    if len(sequence) >= 9:
                        if len(sequence)%3 == 0:
                            CAI_value = str(instance.cai_for_gene(sequence))
                            out_file.write(gene_id + "\t" + CAI_value + "\n")
                        elif len(sequence)%3 == 1:
                            sequence = sequence[1:]
                            CAI_value = str(instance.cai_for_gene(sequence))
                            out_file.write(gene_id + "\t" + CAI_value + "\n")
                        elif len(sequence)%3 == 2:
                            sequence = sequence[2:]
                            CAI_value = str(instance.cai_for_gene(sequence))
                            out_file.write(gene_id + "\t" + CAI_value + "\n")
                    elif len(sequence) <= 9:
                        pass
                    else:
                        print "Something is terribly wrong. Check the file."
            else:
                print "There is an error >>> Check the file's names and their content."

def create_file():
    """ Creates files in the current working directory. Files need to be named during the process.
     Function returns full path to the new file."""

    name = raw_input("You are naming the output files of CAI_calculation function."
    "Enter name for output file (should be: caipy_date_used data set(standard/denovo/nongenes).txt):")
    call(["touch", name])
    path = os.getcwd()
    output_file = path + "/" + name
    return output_file


if __name__ == "__main__":
    function = 'main'
    doc = locals()[function].__doc__
    if len(sys.argv) != 4:
        print 'Bad number of arguments: {0}'.format(len(sys.argv) - 1)
        print 'Module %s%s\nFunction %s \n %s' %(__file__, __doc__, function, doc )
        sys.exit(1)
    main(*sys.argv[1:])

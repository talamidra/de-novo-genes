#!/usr/bin/env python
import sys
import os
import matplotlib
import numpy as np
import matplotlib.pyplot as plt
import pylab as P


def main(standard, denovo, nongenes):
    """ Creates graph out of CAI values for each gene in three data sets. These sets
     are generated from files, which are the results of cai.py.
    Arguments:
    highly_expressed_genes = file with names of highly expressed genes and their CAI values,
    denovo = file with names of our putative de novo genes and their CAI values,
    nongenes =  file with names of noncoding intergenic sequences and their CAI values."""

    datasets = [extract_values(subor) for subor in standard, denovo, nongenes]

    make_graph(datasets)
    make_histogram(datasets)
    make_boxplot(datasets)

def extract_values(path):
    """ Takes just the values (not the names) from the files and add them into the list."""
    dataset = []
    with open(path) as open_file:
        for line in open_file:
            stripped_lines = line.rstrip()
            split_lines = stripped_lines.split("\t")
            dataset.append(split_lines[1])

        return dataset



def make_graph(datasets):
    """ Takes the data sets, sorts them and makes graph out of their values.
    Arguments: data sets are the results of extract_values function. """

    path = os.getcwd()
    standard_set = sorted(datasets[0])
    denovo_set = sorted(datasets[1])
    nongenes_set = sorted(datasets[2])

    plt.figure()
    plt.plot(standard_set,"r", label = "highly expressed genes")
    plt.plot(denovo_set,"b", label = "predicted ORFs")
    plt.plot(nongenes_set,"g", label = "noncoding intergenic sequences")
    plt.ylabel('CAI values')
    legend = plt.legend(fontsize='small')
    legend.get_frame()
    plt.savefig(path + "/cai_graph.jpg")

def make_histogram(datasets):
    """Takes the data sets and makes histogram out of their values.
    Each type of genes (data_set) has its own bar,
    amount of the genes in the interval used is normalized.
    Arguments: data sets are the results of extract_values function. """

    path = os.getcwd()
    standard_set = np.float64(datasets[0])
    denovo_set = np.float64(datasets[1])
    nongenes_set = np.float64(datasets[2])

    P.figure()


    bins = [a/10.0 for a  in range(0,11,1)]

    n, bins, patches = P.hist([standard_set, denovo_set, nongenes_set], bins,
    normed=True, histtype='bar', color = ["red", "green", "blue"],
    label= ["standard", "ORFs", "nongenes"])
    P.xticks(bins)
    P.legend(loc='upper left')
    P.xlabel('CAI value intervals')
    P.ylabel("normalized amount of genes in CAI value intervals")
    P.savefig(path + "/cai_histogram.jpg")

def make_boxplot(datasets):

    path = os.getcwd()
    standard_set = np.float64(datasets[0])
    denovo_set = np.float64(datasets[1])
    nongenes_set = np.float64(datasets[2])

    plt.figure()
    data = [standard_set, denovo_set, nongenes_set]

    plt.xlabel("data sets of genes")
    plt.ylabel('CAI value')
    plt.boxplot(data, showmeans=True)
    plt.xticks([1,2,3], ['highly expressed genes','putative denovo genes','noncoding sequences'],
    size = "small", color = "blue")
    plt.savefig(path + "/cai_boxplot.jpg")

if __name__ == "__main__":
    function = 'main'
    doc = locals()[function].__doc__
    if len(sys.argv) != 4:
        print 'Bad number of arguments: {0}'.format(len(sys.argv) - 1)
        print 'Module %s%s\nFunction %s \n %s' %(__file__, __doc__, function, doc )
        sys.exit(1)
    main(*sys.argv[1:])

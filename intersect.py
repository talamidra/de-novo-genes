#!/usr/bin/env python
import sys
from subprocess import call

def main(gene_bed, orfan_bed, total_out, partial_out, nonoverlap_out):
    ''' Arguments:
    gene_bed = file.bed with annotated genes
    orfan_bed = file.bed with putative de novo genes
    total_out = file.bed for totally overlapping genes (total.bed)
    partial_out = file.bed for partially overlapping genes (partial.bed)
    nonoverlap_out = file.bed for nonoverlapping genes (no.bed)
    Functions call intersect (Bedtools) with different parameters, result is
    written in the prepared files.'''

    intersect_total(gene_bed, orfan_bed, total_out)
    intersect_partial(gene_bed, orfan_bed, partial_out)
    intersect_no(gene_bed, orfan_bed, nonoverlap_out)
    gene_amount(total_out,partial_out,nonoverlap_out)

def intersect_total(gene_bed, orfan_bed, total_out):
    ''' Totally overlapping genes with there coordinates and coresponding
    annotated genes are written in the total_out.'''

    with open(total_out, "w") as write_file:
        call(['intersectBed',
                '-a', orfan_bed,
                '-b', gene_bed,
                '-f','0.7',
                '-wo'],
                stdout = write_file)


def intersect_partial(gene_bed, orfan_bed, partial_out):
    ''' Partially overlapping genes with there coordinates and coresponding
    annotated genes are written in the partial_out.'''

    with open(partial_out,'w') as write_file:
        call(['intersectBed',
                '-b', gene_bed,
                '-a', orfan_bed,
                '-f','0.05',
                '-s'
                '-wo'],
                stdout = write_file)

def intersect_no(gene_bed, orfan_bed, nonoverlap_out):
    ''' Genes that does not overlap any annotated genes (with there coordinates)
     are written in the nonoverlap_out.'''

    with open(nonoverlap_out, 'w') as write_file:
        call(['intersectBed',
                '-b', gene_bed,
                '-a', orfan_bed,
                '-wo',
                '-v'],
                stdout = write_file)


def gene_amount(total_out, partial_out, nonoverlap_out):
    '''count lines (genes) in the files which are the results of the intersect
    functions'''

    with open(total_out) as open_file:
        count = sum(1 for line in open_file)
        print "There are %s putative de novo gene totally overlapping annotated genes." % count

    with open(partial_out) as open_file:
        count = sum(1 for line in open_file)
        print "There are %s putative de novo gene partially overlapping annotated genes." % count

    with open(nonoverlap_out) as open_file:
        count = sum(1 for line in open_file)
        print "There are %s putative de novo gene that does not overlap any annotated genes." % count

if __name__ == "__main__":
    function = 'main'
    doc = locals()[function].__doc__
    if len(sys.argv) != 6:
        print 'Bad number of arguments: {0}'.format(len(sys.argv) - 1)
        print 'Module %s%s\nFunction %s \n %s' %(__file__, __doc__, function, doc )
        sys.exit(1)
    main(*sys.argv[1:])

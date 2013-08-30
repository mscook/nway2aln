nway2aln
========

Given a Nesoni n-way SNP comparison file produce a mfa alignment file


Examples
--------

Example (with reference in Nesoni n-way)::
    
    $ ./nway2aln.py XXXX.all.withref XXXX.fa


Example (with reference not in Nesoni n-way)::

    $ ./nway2aln.py XXXX.all.withref XXXX.fa --without_ref


Usage
-----

Something like::

    ./nway2aln -h
    usage: nway2aln [-h] [-v] [--without_ref] infile outfile

    nway2aln v0.2 - Given a Nesoni n-way SNP comparison file produce a mfa
    alignment file (https://github.com/mscook/nway2aln)

    positional arguments:
      infile         Full path to the input nway
      outfile        Full path to the output alignment file

    optional arguments:
      -h, --help     show this help message and exit
      -v, --verbose  verbose output
      --without_ref  Is the reference in the nway (default = True)


Notes
-----

Please be aware of:
    * This has not been tested yet with files that include the SNP 
      effects. Report problems please.
    * a lookup table ('args.outfile'.lookup) is stored so that you can map the 
      SNP positions to the reference positions

#!/usr/bin/env python

#Copyright 2011-2013 Mitchell Jon Stanton-Cook & Elizabeth Skippington 
#Licensed under the #Educational Community License, Version 2.0 (the "License");
#you may not use this file except in compliance with the License. You may
#obtain a copy of the License at
#
##http://www.osedu.org/licenses/ECL-2.0
#
##Unless required by applicable law or agreed to in writing,
#software distributed under the License is distributed on an "AS IS"
#BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express
#or implied. See the License for the specific language governing 
#permissions and limitations under the License. 

"""
Utilities for manipulating data for phylogenetics- standalone nway2aln
"""

import __init__ as meta

import sys, os, traceback, argparse
import time


epi = "Licence: %s by %s <%s>" % (meta.__license__,
                                  meta.__author__,
                                  meta.__author_email__)
__doc__ = " %s v%s - %s (%s)" % (meta.__title__,
                                 meta.__version__,
                                 meta.__description__,
                                 meta.__url__)

def nway_to_alignment(args):
    """
    Produce a mfa alignment file from a Nesoni n-way SNP comparison file
   
    :param args: a argparse args object (including: args.infile, args.outfile, 
                 args.without_ref)

    :type args: argparse args
    """
    # Initialise 
    args.infile   = os.path.expanduser(args.infile)
    args.outfile  = os.path.expanduser(args.outfile)
    count    = 0
    lookup_table = {}
    
    if not os.path.isfile(args.infile):
        print "Please specify a valid Nesoni n-way SNP comparison file"
        sys.exit(1)
    else:
        f = open(args.infile, 'r')
        line = f.readline()
        xx = line.strip().split()
        if args.without_ref:
            no_of_strains = int(float(len(xx) - 5)/float(3) + 1)
        else:
            no_of_strains = int(float(len(xx) - 5)/float(3))
        n = 4 + no_of_strains
        m = 3 + no_of_strains
        names = xx[4:n]
        #Set up an empty alignment block
        matrix = []
        for i in range(no_of_strains):
            matrix.append('')
        line = f.readline()
        while(line):
            xx = line.strip().split()
            type = xx[2]
            if type == 'substitution':
                yy = xx[3:m]
                count = count + 1
                # Store for lookup
                lookup_table[int(xx[1])] = count
                for i in range(len(yy)):
                    tmp = matrix[i]
                    matrix[i] = tmp + yy[i]
            line = f.readline()
        f.close()
        # Write alignment to a file 
        f  = open(args.outfile, 'w')
        f2 = open(args.outfile+'.lookup', 'w')
        f2.write(str(lookup_table))
        for i in range(len(matrix)):
            f.write('>'+names[i]+'\n')
            f.write(matrix[i]+'\n')
        f.close()
        print "The alignment contains %i columns" % (count)


if __name__ == '__main__':
    try:
        start_time = time.time()
        parser = argparse.ArgumentParser(description=__doc__, epilog=epi)
        parser.add_argument('-v', '--verbose', action='store_true',
                                default=False, help='verbose output')
        parser.add_argument('--without_ref',action='store_false',
                                default=True, help=('Is the reference in the '
                                    'nway (default = True)'))
        parser.add_argument('infile', action='store',
                                help=('Full path to the input nway'))
        parser.add_argument('outfile', action='store',
                                help=('Full path to the output alignment file'))
        parser.set_defaults(func=nway_to_alignment)
        args = parser.parse_args()
        if args.verbose:
            print "Executing @ " + time.asctime()
        args.func(args)
        if args.verbose:
            print "Ended @ " + time.asctime()
            print 'Exec time minutes %f:' % ((time.time() - start_time) / 60.0)
        sys.exit(0)
    except KeyboardInterrupt, e: # Ctrl-C
        raise e
    except SystemExit, e: # sys.exit()
        raise e
    except Exception, e:
        print 'ERROR, UNEXPECTED EXCEPTION'
        print str(e)
        traceback.print_exc()
        os._exit(1)

#!/usr/bin/env python

# plotTxtFiles
#
# Usage:
#  ./plotTxtFiles { -i dataFile.txt }+  -o outputImage.png -x XLabel -T title -f From -t To -v
#
# Plots various data files together. Output goes into outputImage.png. Title is specified via -T.
# The abscissas label is specified via -x. Options -f From and -t To select lines [From:To+1] for printing.
#
# Versions
#  v1.0 (June 12, 2018)
# 

import numpy as np
import sys

VERSION = 1.0
DATE = '2018-06-12'

import os, sys
import numpy as np
import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt


def plotnArrays(fds, fns, oFile, title, xlabel):
    ps = [ 'rs', 'g^', 'bs', 'r^', 'gs', 'b^' ]
    lps = len(ps)

    l=len(fds)
    # print 'plotting {0} arrays (output=\'{1}\')\n'.format(l,oFile)
    lenX=fds[0].size
    
    minY = np.nanmin(fds[0])
    maxY = np.nanmax(fds[0])
    for i in range(1,l):
        minZ = np.nanmin(fds[i])
        maxZ = np.nanmax(fds[i])
        Min = minY if minY < minZ else minZ
        Max = maxZ if maxZ > maxY else maxY

    sz=Max-Min # add extra border
    sz=sz/50
    Min -= sz
    Max += sz
    fig = plt.figure(figsize=(10,7))
    plt.subplot(111)
    plt.axis([0, lenX, Min, Max])
    plt.xlabel(xlabel)
    plt.title(title)

    '''
    lst = []
    for i in range(l):
        lst.append(fds[i])
        lst.append(ps[i % lps])
    tpl = tuple(lst)
    print 'Plotting tuple is {0}'.format(tpl)
    plt.plot(*tpl)
    '''

    for i in range(l):
        plt.plot(fds[i], ps[i % lps], label=str(i))

    plt.savefig(oFile)
    plt.clf()
    plt.close(fig)

def dumpArray(r, file):
    s=r.size
    try:
        with open(file, 'w') as g:
            for i in range(s):
                g.write('{0}\n'.format(r[i]))
    except:
       sys.stderr.write('dumpArray failed\n')
       return False
    return True
        
#****************************************************************************
## Main entry point
#{
if __name__ == '__main__' :

    argv = sys.argv
    argc = len(argv)

    if argc == 1:
        sys.stderr.write('At least one file must be specified on the command line. Bailing out...\n')
        sys.exit(-1)

    # Now we know that we have args on the command line

    oFile = 'plotTxtFiles/output.png'
    From = 0
    To = 0
    err = False
    title = 'LAI vs SM (-0.2: val == 248)'
    xlabel = 'days'
    verbose=False

    i = 1
    fns = []
    while i < argc :
        arg = argv[i]
        if len(arg) >= 2:
            if arg[0] == '-':
                arg = arg[1:]

                if arg == 'i':
                    i += 1
                    fns.append(argv[i])
                elif arg == 'o':
                    i += 1
                    oFile = argv[i]
                elif arg == 'x':
                    i += 1
                    xlabel = argv[i]
                elif arg == 'f':
                    i += 1
                    From = int(argv[i])
                elif arg == 't':
                    i += 1
                    To = int(argv[i])
                elif arg == 'T':
                    i += 1
                    title = argv[i]
                elif arg == 'v':
                    verbose=True
                else:
                    sys.stderr.write('Erroneous argument caught: -{0}\n'.format(arg))
                    err = True
                    break
            else:
                print arg
                err = True
                break
        else:
            print arg
            err = True
            break
        i += 1

    if err:
        sys.stderr.write('Error in the commandline arguments. Bailing out...\n')
        sys.exit(-1)

    if verbose:
        print 'Input files: {0}'.format(fns)
        print 'Output file: {0}'.format(oFile)
        print 'Title      : {0}'.format(title)
        print 'xlabel     : {0}'.format(xlabel)
        if From != 0 or To != 0:
            print 'From: {0}'.format(From)
            print 'To  : {0}'.format(To)

    cwd = os.getcwd()

    fds = list(fns)
    l = len(fns)
    for i in range(l):
        try:
            fds[i] = open(fns[i])
        except:
            sys.stderr.write('File {0} could not be accessed. Bailing out...\n'.format(fns[i]))
            sys.exit(-1)

    # Now we know that all the files in fns[] are open and their corresponding fd is in fds[]

    for i in range(l):
        lines = fds[i].readlines()
        fds[i].close()
        if From != 0 or To != 0:
            lines = lines[From:To+1]
        fds[i] = np.array ( [ float(line.rstrip()) for line in lines ] )

    # Now we know that the contents of all the files in fns[] is in the numpy arrays fds[]

    plotnArrays(fds, fns, oFile, title, xlabel)
#} end of main and file

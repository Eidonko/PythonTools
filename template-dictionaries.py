#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function

__author__    = "Eidon (Eidon@tutanota.com)"
__module__    = "template-dictionary.py"
__version__   = "1.1"
__revision__  = filter(str.isdigit, "$Revision: 1 $")
__date__      = filter(str.isalnum, "$Date: 2018-05-30 $")

VERSION = '1.1'
DATE = '2018-06-18'

# @author Eidon (Eidon@tutanota.com)
# @details Given a file with parameter dictionaries (in what follows, a 'template') and a set
#          of 'key=value' associations, this module searches the template for 'key=...' statements
#          and updates them accordingly.
#
# @Example       ./template-dictionary.py \
#                   --input input.template  --output params.py \
#                   --param    steps         43          \
#                   --param    region       "(103, 2)"   \
#                   --paramstr product       soda 
#
#                1) input.template is scanned for lines such as
#                             'steps' = '...',
#                             'region' = '...',
#                             'product' = '...',
#                   where '...' means whatever string enclosed in ' characters
#                2) Every occurrence of the above is changed into
#                             'steps' = 43,
#                             'region' = (103, 2),
#                             'product' = "soda",
#                   Please note the use of quotes in the third line.
#                3) The output goes into file params.py
#
# Note: the difference between --param and --paramstr is that in the latter case the value is quoted
#

import sys, os
import re

input=None
output=None

argv = list(sys.argv)
argc = len(argv)

# %SITE
# %STARTDATE
# %ENDDATE

def options():
    sys.stderr.write('Options: --start[_date] date   --end[_date] date\n')
    sys.stderr.write('         [ --input file ] [ --output file ]\n')
    sys.stderr.write('         [ --param key value ] [ --paramstr key value ]\n')

if argc == 1:
    options()
    sys.exit(-1)

# argc > 1

start_date = None
end_date = None
site = 0
verbose = False

param = {}
occur = {}
pstr  = {}

i=1
while i<argc:
    # print 'argv[{0}] = {1}'.format(i, argv[i])
    arg = argv[i].lower()
    # print('arg = {}'.format(arg))

    if    arg == '--param' :
          # print 'arg + 1 and +2: {0}, {1}'.format(argv[i+1], argv[i+2])
          if i+2 < argc:
              # if  argv[i+2][0] == r"'" and argv[i+2][-1] == r"'" :
              #     argv[i+2] = argv[i+2][1:-1]
              param[argv[i+1]] = argv[i+2]
              occur[argv[i+1]] = 0
              pstr [argv[i+1]] = False
          i += 2
    elif  arg == '--paramstr' :
          if i+2 < argc:
              # if  argv[i+2][0] == r"'" and argv[i+2][-1] == r"'" :
              #     argv[i+2] = argv[i+2][1:-1]
              param[argv[i+1]] = argv[i+2]
              occur[argv[i+1]] = 0
              pstr [argv[i+1]] = True
          i += 2
    elif  arg == '--input' :
          if i+1 < argc:
              input = argv[i+1]
          i += 1
    elif  arg == '--output' :
          if i+1 < argc:
              output = argv[i+1]
          i += 1
    elif  arg == '--verbose' :
          verbose = True
    else:
          options()
          sys.exit(-1)
    i += 1


try:
    with open(input) as f:
        lines = f.readlines()
except:
    sys.stderr.write('Problems accessing file %s.\n' %(input))
    sys.exit(-2)


p = re.compile(r"(\s*)(')([a-zA-Z_]+)(')(\s*)(:)(\s*)(')(.*)(')(.*)$")
# <space>  'key'      : 'value'     <whatever>
# group(1) 'group(3)' : 'group(9)'

# lines = [ line.replace('%STARTDATE', start_date).replace('%ENDDATE', end_date).replace('%SITE', str(site)) for line in lines ]

l = len(lines)
i = 0
while i < l:
    #for each input line
    line = lines[i]

    # does the line specify a 'key' : 'value' pair?
    m = p.match(line)

    # if so,
    if  m:
        # for each key provided by the user:
        for key in param:
            # if the key is present in the current line
            if key in line:
                # reconstruct the line with the new value specified by the user
                if pstr[key]:
                    #       space         '        key        '    space          : '       key         ',
                    line = m.group(1) + r"'" + m.group(3) + r"'" + m.group(5) + r": '" + param[key] + r"'," + '\n'
                else:
                    #       space         '        key        '    space          :        key           ,
                    line = m.group(1) + r"'" + m.group(3) + r"'" + m.group(5) + r": " + param[key] + r"," + '\n'
                # and store back the line in the list
                lines[i] = line
                occur[key] += 1
    # next line
    i += 1
       

try:
    with open(output, 'w') as g:
        g.writelines(lines)
except:
    sys.stderr.write('Problems accessing file %s.\n' %(output))
    sys.exit(-3)

if verbose:
    sys.stderr.write('Process summary:\n')

if verbose:
    for key in param:
        if pstr[key]:
            sys.stderr.write(' - Key %s has been replaced %d times with value \'%s\'.\n' %(key, occur[key], param[key]))
        else:
            sys.stderr.write(' - Key %s has been replaced %d times with value %s.\n' %(key, occur[key], param[key]))

if verbose:
    sys.stderr.write('Process concludes successfully (\'{}\').\n'.format(output))

# EoF (template2params.py)

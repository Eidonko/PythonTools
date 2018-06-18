#!/usr/bin/python

# Class megapix
#
# Megapixel image management module, designed and written by Eidon (Eidon@tutanota.com), August 2017.
#
# A megapixel image has physical dimensions ((dim x dim) pixels) and "logical" dimensions ((megadim x megadim) megapixels).
# Each megapixel corresponds to a cluster of physical pixels in some (dim x dim) reference image.
# On initialization, the user specifies dim and a redundancy factor, redun. This defines a megapixel size of
# (redun x redun) physical pixels. 
# Class megapix manages the translation from megapixels to pixels. In particular,
# - method get(megarow, megacol) returns the row and col of the physical pixel at the center of the megapixel, while
# - method getRowCol(megarow, megacol) returns a list of (row, col) couples with the locations of all the physical pixels
#   corresponding to the mentioned megapixel. 
#
# Limitations:
# The current version only works with square images and assumes that the megapixel image fits perfectly into the physical image
#
# Versions
#  v1.0 (August 28, 2017)
#  v1.1 (August 30, 2017)
# 

import numpy as np
import sys

VERSION = 1.1
DATE = '2017-08-30'

class megapix:
    errMsg01 = 'megapix::__init__: invalid initialization parameters'
    errMsg02 = 'megapix::__init__: trueRedun should be in [1, redun]'
    errMsg03 = 'megapix::__init__: trueRedun should be an odd number'
    
    ########################################################################################################################
    # @brief Class constructor
    # @param dim               (int)                Specifies that the reference, "physical" image is a (dim x dim) image 
    # @param redun             (int)                defines a megapixel size of redun x redun physical pixels
    # @param trueRedun         (int)                specifies the region in which the physical pixel is replicated
    def __init__(self, dim, redun, trueRedun) :
        self.msg       = None
        self.dim       = int(dim)
        self.redun     = int(redun)
        self.trueRedun = int(trueRedun)
        self.megadim   = 0
        
        if self.redun != 0 :
            self.megadim  = self.dim / self.redun
        else:
            self.msg = self.errMsg01
            return

        if self.dim < 1 or self.redun < 1 :
            self.msg = self.errMsg01
            self.megadim = 0
            return

        if self.trueRedun < 1 or self.trueRedun > self.redun :
            self.msg = self.errMsg02
            self.megadim = 0
            return
        if self.trueRedun % 2 == 0:
            self.msg = self.errMsg03
            self.megadim = 0
            return
#       
#       if self.dim - self.megadim * self.redun != 0:
#           self.msg = self.errMsg01
#           self.megadim = 0
#           return
            
        #self.displace = int(self.redun / 2)
        self.displace = int(self.trueRedun / 2)
        self.cells    = [ [ None, None ] ] * (self.trueRedun * self.trueRedun)
        return
 
    ##########################################
    # @brief returns the latest error messages
    # @return ditto
    def getErr(self):
        return self.msg
    
    #####################################################
    # @brief returns the dimension of the "logical" image
    # @return ditto
    def getMegadim(self):
        return self.megadim
    
    ##########################################################################################################
    # @brief returns the row and col of the physical pixel at the center of a specified megapixel
    # @param megarow           (int)                row    of a megapixel 
    # @param megacol           (int)                column of a megapixel
    # @return False on failure, otherwise the row and col of the physical pixel at the center of the megapixel
    def get(self, megarow, megacol):
        if self.megadim == 0:            
            msg = 'get: megapixel image ({%d}x{%d}) does not fit within image ({%d}x{%d})' % (self.megadim,self.megadim, self.dim,self.dim) 
            if self.msg != None:
                msg = msg + '\n\t(cf: ' + self.msg + ')'
            self.msg = msg     
            return False
        if megarow < 0 or megarow >= self.megadim:
            msg = 'get: input megarow (%d) should be in [0, %d[' % (megarow, self.megadim)
            if self.msg != None:
                msg = msg + '\n\t(cf: ' + self.msg + ')'
            self.msg = msg
            return False
        if megacol < 0 or megacol >= self.megadim:
            msg = 'get: input megacol (%d) should be in [0, %d[' % (megacol, self.megadim)
            if self.msg != None:
                msg = msg + '\n\t(cf: ' + self.msg + ')'
            self.msg = msg
            return False
        r = megarow * self.redun + self.displace
        c = megacol * self.redun + self.displace
        return [r, c]
    
    #################################################################################################################
    # @brief returns a list of (row, col) couples of all the physical pixels corresponding to the mentioned megapixel 
    # @param megarow           (int)                row    of a megapixel 
    # @param megacol           (int)                column of a megapixel
    # @return False on failure, otherwise a list of [ row , col ] couples
    def getRowCol(self, megarow, megacol, Verba=False):
        ret = self.get(megarow, megacol)
        if not ret:
            self.msg = 'getRowCol: get failed (%s)' % (self.msg)
            return False
        [r, c] = ret
        i = 0
        for rr in range(r - self.displace, r + self.displace + 1):
            for cc in range(c - self.displace, c + self.displace + 1):
                if Verba:   print 'cells[{2}] = [{0},{1}]'.format(rr,cc,i)
                self.cells[i] = [ rr, cc ]
                i = i + 1
        return self.cells


def Red(prt): return "\033[91m%s\033[00m" % (prt)
def Green(prt): return "\033[92m%s\033[00m" % (prt)
def Yellow(prt): return "\033[93m%s\033[00m" % (prt)
def LightPurple(prt): return "\033[94m%s\033[00m" % (prt)
def Purple(prt): return "\033[95m%s\033[00m" % (prt)
def Cyan(prt): return "\033[96m%s\033[00m" % (prt)
def LightGray(prt): return "\033[97m%s\033[00m" % (prt)
def Black(prt): return "\033[98m%s\033[00m" % (prt)

#****************************************************************************
## Main entry point
#
if __name__ == "__main__":

    # from termcolor import colored

    print 'Test program for class megapixel'
    dim       = int(raw_input("Please enter the image dimension: "))
    redun     = int(raw_input("Please enter the mask dimension: "))
    trueRedun = int(raw_input("Please enter the true mask dimension: "))
    mp = megapix(dim, redun, trueRedun)
    if mp.getErr() != None:
        print 'Megapix failed and returned message "{0}"'.format(mp.getErr())
        sys.exit(-1)
    
    array = np.empty([dim,dim], dtype='int')
    array.fill(-1)

    succ = 1
    megaDim = mp.getMegadim()
    for i in range(megaDim):
        for j in range(megaDim):
            cells = mp.getRowCol(i, j)
            if cells == False:
                print 'Sorry, getRowCol failed'
                sys.exit(-1)
            for cell in cells:
		r, c = cell
                array[r][c] = succ
            succ = succ + 1

    rjustSize = len(str(succ-1))
    if rjustSize == 1: rjustSize = 2	# because we use "-1" too, thus min size is 2

    for i in range(dim):
        for j in range(dim):
          if array[i][j] != -1 :
              #print '{0} '.format(colored(repr(array[i][j]).rjust(rjustSize)),'green'),
              print '{0} '.format(Red(repr(array[i][j]).rjust(rjustSize)),'green'),
          else :
              print '{0} '.format(repr(-1).rjust(rjustSize)),
          # print '{0} '.format(repr(array[i][j]).rjust(rjustSize)),
        print ''

    print 'Megapixel test program ends.'
    sys.exit(0)

'''
python megapixel.py
Test program for class megapixel
Please enter the image dimension: 12
Please enter the mask dimension: 4
Please enter the true mask dimension: 3
 1   1   1  -1   2   2   2  -1   3   3   3  -1
 1   1   1  -1   2   2   2  -1   3   3   3  -1
 1   1   1  -1   2   2   2  -1   3   3   3  -1
-1  -1  -1  -1  -1  -1  -1  -1  -1  -1  -1  -1
 4   4   4  -1   5   5   5  -1   6   6   6  -1
 4   4   4  -1   5   5   5  -1   6   6   6  -1
 4   4   4  -1   5   5   5  -1   6   6   6  -1
-1  -1  -1  -1  -1  -1  -1  -1  -1  -1  -1  -1
 7   7   7  -1   8   8   8  -1   9   9   9  -1
 7   7   7  -1   8   8   8  -1   9   9   9  -1
 7   7   7  -1   8   8   8  -1   9   9   9  -1
-1  -1  -1  -1  -1  -1  -1  -1  -1  -1  -1  -1
Megapixel test program ends.

python megapixel.py
Test program for class megapixel
Please enter the image dimension: 16
Please enter the mask dimension: 5
Please enter the true mask dimension: 3
 1   1   1  -1  -1   2   2   2  -1  -1   3   3   3  -1  -1  -1
 1   1   1  -1  -1   2   2   2  -1  -1   3   3   3  -1  -1  -1
 1   1   1  -1  -1   2   2   2  -1  -1   3   3   3  -1  -1  -1
-1  -1  -1  -1  -1  -1  -1  -1  -1  -1  -1  -1  -1  -1  -1  -1
-1  -1  -1  -1  -1  -1  -1  -1  -1  -1  -1  -1  -1  -1  -1  -1
 4   4   4  -1  -1   5   5   5  -1  -1   6   6   6  -1  -1  -1
 4   4   4  -1  -1   5   5   5  -1  -1   6   6   6  -1  -1  -1
 4   4   4  -1  -1   5   5   5  -1  -1   6   6   6  -1  -1  -1
-1  -1  -1  -1  -1  -1  -1  -1  -1  -1  -1  -1  -1  -1  -1  -1
-1  -1  -1  -1  -1  -1  -1  -1  -1  -1  -1  -1  -1  -1  -1  -1
 7   7   7  -1  -1   8   8   8  -1  -1   9   9   9  -1  -1  -1
 7   7   7  -1  -1   8   8   8  -1  -1   9   9   9  -1  -1  -1
 7   7   7  -1  -1   8   8   8  -1  -1   9   9   9  -1  -1  -1
-1  -1  -1  -1  -1  -1  -1  -1  -1  -1  -1  -1  -1  -1  -1  -1
-1  -1  -1  -1  -1  -1  -1  -1  -1  -1  -1  -1  -1  -1  -1  -1
-1  -1  -1  -1  -1  -1  -1  -1  -1  -1  -1  -1  -1  -1  -1  -1
Megapixel test program ends.


'''

'''
    while True:
        megarow = raw_input("\nPlease enter the megarow (-1 to end): ")
        if megarow == '-1':
            break
        megacol = raw_input("Please enter the megacol (-1 to end): ")
        if megacol == '-1':
            break
        megarow = int(megarow)
        megacol = int(megacol)
        cell = mp.get(megarow, megacol)
        if not cell:
            print 'megapixel method get has failed:\n\t\'{0}\''.format(mp.getErr())
            continue
        cells = mp.getRowCol(megarow, megacol)
        if not cells:
            print 'megapixel method getRowCol has failed:\n\t\'{0}\''.format(mp.getErr())
            continue
        print 'megapixel ({0},{1}) corresponds to a frame centered at {2} whose cells are {3}'.format(megarow, megacol, cell, cells)

    print "Megapixel test program ends."
'''

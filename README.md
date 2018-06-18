# PythonTools
A set of utilities written in python

## Utility template-dictionaries.py 
Given a file with parameter dictionaries (in what follows, a 'template') and a set
of 'key=value' associations, this module searches the template for 'key=...' statements
and updates them accordingly.

Example:

      ./template-dictionary.py \
                   --input input.template  --output params.py \
                   --param    steps         43          \
                   --param    region       "(103, 2)"   \
                   --paramstr product       soda

- input.template is scanned for lines such as

    'steps' = '...',
    'region' = '...',
    'product' = '...',

where '...' means whatever string enclosed in ' characters

- Every occurrence of the above is changed into

    'steps' = 43,
    'region' = (103, 2),
    'product' = "soda",

Please note the use of quotes in the third line.

- The output goes into file params.py

Note: the difference between --param and --paramstr is that in the latter case the value is quoted


## Class megapixel
A megapixel image has physical dimensions ((dim x dim) pixels) and _logical_ dimensions ((megadim x megadim) megapixels).
Each megapixel corresponds to a cluster of physical pixels in some (dim x dim) reference image.
On initialization, the user specifies dim and a redundancy factor, redun. This defines a megapixel size of (redun x redun) physical pixels.
Class megapix manages the translation from megapixels to pixels. In particular,
- method get(megarow, megacol) returns the row and col of the physical pixel at the center of the megapixel, while
- method getRowCol(megarow, megacol) returns a list of (row, col) couples with the locations of all the physical pixels
  corresponding to the mentioned megapixel.

Limitations:
The current version only works with square images and assumes that the megapixel image fits perfectly into the physical image


## Utility plotTxtFiles

Usage:

    ./plotTxtFiles { -i dataFile.txt }+  -o outputImage.png -x XLabel -T title -f From -t To -v

Plots various data files together. Output goes into outputImage.png. Title is specified via -T. The abscissas label is specified via -x. Options -f From and -t To select lines [From:To+1] for printing.


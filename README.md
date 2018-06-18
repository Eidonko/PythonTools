# PythonTools
A set of utilities written in python

## template-dictionaries.py 
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

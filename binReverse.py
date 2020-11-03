#!/usr/bin/python
import sys
import os

# binReverse
# 0fabris
# 11/2020
# script to reverse the content of a binary file into another

if len(sys.argv) < 2:
    exit("use: "+sys.argv[0]+" binaryname [filedest = 'rbinaryname']")

fname = sys.argv[1]

#if not specified destination file name use 'r' + filename
rfname = ('r'+fname) if len(sys.argv) > 1 else sys.argv[2]

#go to the last byte and write every single byte in reverse
with open(rfname,'wb') as f1:
    with open(fname,"rb") as f:
        f.seek(0,2) #end of file
        while f.tell() != 0: #not position 0
            f.seek(-1,1) #go back 1 char
            f1.write(f.read(1)) # read it 
            f.seek(-1,1) # go back another

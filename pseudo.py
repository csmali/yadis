#!/usr/bin/python

import sys

filename= str(sys.argv[1])


C_PROGRAM_INIT="import <stdio.h> \n     void int(){ \n"
C_PROGRAM_FINAL="     }\n"



file = open(filename, "r") 
for line in file: 
	print line,

print "\n\n"
print C_PROGRAM_INIT,C_PROGRAM_FINAL
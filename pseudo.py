#!/usr/bin/python

import sys

filename= str(sys.argv[1])

TAB="     "
NEW_LINE= "\n"
C_PROGRAM_START="import <stdio.h> \n     void int(){ \n"
C_PROGRAM_END="     }\n"
C_PROGRAM = ""
lines=[]
register_dict={}
register_index={}
register_val={}
C_PROGRAM = C_PROGRAM_START
i = 0
file = open(filename, "r") 
for line in file: 
	print i 
	print line
	line = line.split()

	#print line,

	
	# initializing array

	if line[1]=="WORD":

		arrayname=line[0]
		arraysize=line[3]
		C_PROGRAM = C_PROGRAM + TAB+TAB+"int "+ arrayname + "["+arraysize+"];"+NEW_LINE

	if line[0]=="lea":

		register=line[1].split(',')[0]
		arrayname=line[1].split(',')[1]
		register_dict[line[1].split(',')[0]]=line[1].split(',')[1]
		register_index[line[1].split(',')[0]]=0

	if line[0]=="add":

		register = line[1].split(',')[0]
		if "[" in register: 
			register=register[1:-1]
		if register in register_dict:
			if("0x" in line[1].split(',')[1]):
				register_index[register]=register_index[register]+int(line[1].split(',')[1][2:],16)
			else:
				register_index[register]=register_index[register]+int(line[1].split(',')[1])/4


		#address change
		if "[" in line[1].split(',')[0]: 
			C_PROGRAM = C_PROGRAM + TAB+TAB+register_dict[register]+"["+str(register_index[register])+"]"+str(int(line[1].split(',')[1][2:],16))
		#value change
		else:
			if("0x" in line[1].split(',')[1]):
				register_val[register]=str(int(line[1].split(',')[1][2:],16))
	if line[0] == "mov":

		if "0x" in line[1].split(',')[1] :
			register = line[1].split(',')[0]
			constant = str(int(line[1].split(',')[1][2:],16))
			register_val[register]=constant
		

		elif "e" in  line[1].split(',')[1]:
			register = line[1].split(',')[0][1:-1]
			if "[" in line[1].split(',')[0]:
				print "Reg " + register 
				C_PROGRAM = C_PROGRAM + TAB+TAB+register_dict[register]+"["+str(register_index[register])+"]"+register_val[line[1].split(',')[1]]
		
	if line[0] == "mul":

		register = line[1]
		register_val[register] = str(int(register_val["eax"])*int(register_val[register]))
 
	i = i+1

print "\n"

C_PROGRAM = C_PROGRAM+C_PROGRAM_END
print C_PROGRAM
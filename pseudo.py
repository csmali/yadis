#!/usr/bin/python

import sys

filename= str(sys.argv[1])

TAB="     "
NEW_LINE= "\n"
C_PROGRAM_START="import <stdio.h> \n     void main(){ \n"
C_PROGRAM_END="     }\n"
C_PROGRAM = ""
lines=[]
register_dict={}
register_index={}
register_values={}
C_PROGRAM = C_PROGRAM_START
i = 0
file = open(filename, "r") 
for line in file: 
	print 'i',i 
	print line
	line = line.split()
	
	# initializing array
	#if "ebx" in register_index:
	#	print register_index["ebx"]
	if line[1]=="WORD":

		arrayname=line[0]
		arraysize=line[3]
		C_PROGRAM = C_PROGRAM + TAB+TAB+"int "+ arrayname + "["+arraysize+"];"+NEW_LINE

	if line[0]=="lea":

		register=line[1].split(',')[0]
		arrayname=line[1].split(',')[1]
		register_dict[line[1].split(',')[0]]=line[1].split(',')[1]
		register_values[line[1].split(',')[0]]=0
		register_index[line[1].split(',')[0]]=0

	if line[0]=="add":

		register = line[1].split(',')[0]
		if "[" in register: 
			register=register[1:-1]
		if register in register_dict:
			if "[" not in line[1].split(',')[0]:
				if("0x" in line[1].split(',')[1]):
					register_dict[register]=int(register_dict[register])+int(line[1].split(',')[1][2:],16)
				else:
					print register_dict[register]
					register_index[register]=int(register_index[register])+int(line[1].split(',')[1])/4
			

		#address change
		if "[" in line[1].split(',')[0]: 
			C_PROGRAM = C_PROGRAM + TAB+TAB+register_dict[register]+"["+str(register_index[register])+"]="+str(int(line[1].split(',')[1][2:],16))+";"+NEW_LINE
		#value change
		else:
			if("0x" in line[1].split(',')[1]):
				register_val[register]=str(int(line[1].split(',')[1][2:],16))
	if line[0] == "mov":

		if "0x" in line[1].split(',')[1] :
			register = line[1].split(',')[0]
			constant = str(int(line[1].split(',')[1][2:],16))
			register_values[register]=constant
		

		elif "e" in  line[1].split(',')[1]:
			register = line[1].split(',')[0][1:-1]
			if "[" in line[1].split(',')[0]:
				C_PROGRAM = C_PROGRAM + TAB+TAB+register_dict[register]+"["+str(register_index[register])+"]="+str(register_values[line[1].split(',')[1]])+";"+NEW_LINE
		
	if line[0] == "mul":

		register = line[1]
		register_values["eax"] = str(int(register_values["eax"])*int(register_values[register]))
	i = i+1

print "\n"

C_PROGRAM = C_PROGRAM+C_PROGRAM_END
print C_PROGRAM
#!/usr/bin/python

import sys

filename= str(sys.argv[1])

TAB="     "
TAB_COUNTER=1
DOUBLE_TAB=TAB+TAB
NEW_LINE= "\n"
C_PROGRAM_START="void main(){ \n"
C_PROGRAM_END="}\n"
C_PROGRAM = ""
lines=[]
register_dict={}
register_index={}
register_values={}
register_variable={}
last_register=""
number_of_variable=0
boolean_condition_is_zero=False
boolean_condition_is_equal=False
jump_point=""
is_jumping=False
is_branch_added=False
C_PROGRAM = C_PROGRAM_START
temp_output=""
i = 0
file = open(filename, "r") 
for line in file: 
	print 'i',i 
	print line
	line = line.split()
	
	# initializing array
	#if "ebx" in register_index:
	#	print register_index["ebx"]



	if ":" in line[0]:
		C_PROGRAM = C_PROGRAM + TAB+"}"+NEW_LINE
		break

	elif line[0]=="leave":

		continue

	elif line[0]=="ret":

		continue

	elif line[0]=="db":	

		C_PROGRAM = C_PROGRAM + TAB+TAB+"printf("+ line[1]+");"+NEW_LINE

	elif line[1]=="WORD":

		arrayname=line[0]
		arraysize=line[3]
		C_PROGRAM = C_PROGRAM + TAB+"int "+ arrayname + "["+arraysize+"];"+NEW_LINE

	elif line[0]=="lea":

		register=line[1].split(',')[0]
		arrayname=line[1].split(',')[1]
		register_dict[line[1].split(',')[0]]=line[1].split(',')[1]
		register_values[line[1].split(',')[0]]=0
		register_index[line[1].split(',')[0]]=0

	elif line[0]=="add":

		register = line[1].split(',')[0]
		if "[" in register: 
			register=register[1:-1]
		if register in register_dict:
			if "[" not in line[1].split(',')[0]:
				if("0x" in line[1].split(',')[1]):
					register_dict[register]=int(register_dict[register])+int(line[1].split(',')[1][2:],16)
				else:
					#print register_dict[register]
					register_index[register]=int(register_index[register])+int(line[1].split(',')[1])/4
				

			#address change
		if "[" in line[1].split(',')[0]: 
			C_PROGRAM = C_PROGRAM + TAB+register_dict[register]+"["+str(register_index[register])+"]="+str(int(line[1].split(',')[1][2:],16))+";"+NEW_LINE
			#value change
		else:
			if("0x" in line[1].split(',')[1]):
				register_val[register]=str(int(line[1].split(',')[1][2:],16))

	elif line[0] == "mov":

			if "0x" in line[1].split(',')[1] :
				register = line[1].split(',')[0]
				constant = str(int(line[1].split(',')[1][2:],16))
				register_values[register]=constant
			

			elif "e" in  line[1].split(',')[1]:
				register = line[1].split(',')[0][1:-1]
				if "[" in line[1].split(',')[0]:
					C_PROGRAM = C_PROGRAM + TAB+register_dict[register]+"["+str(register_index[register])+"]="+str(register_values[line[1].split(',')[1]])+";"+NEW_LINE

			else:
				register = line[1].split(',')[0]
				register_variable[register]="var"+str(number_of_variable)
				number_of_variable+=1
				C_PROGRAM=C_PROGRAM+TAB+"int "+register_variable[register]+"="+line[1].split(',')[1]+";"+NEW_LINE
				register_values[register]=str(line[1].split(',')[1])
			
	elif line[0] == "mul":

			register = line[1]
			register_values["eax"] = str(int(register_values["eax"])*int(register_values[register]))
		
	elif line[0] == "div": 
			
			register = line[1]
			register_values["edx"]="0"
			#print register_values[register]
			#print register_values["eax"]
			register_values["edx"]=str(int(register_values["eax"])%int(register_values[register]))
			last_register=register

	elif line[0] == "cmp" :

			register = line[1].split(',')[0]
			if register == "edx":
				if "0x" in line[1].split(',')[1] :

					if register_values[register]==str(int(line[1].split(',')[1][2:],16)):
						boolean_condition_is_equal = True
					else:
						boolean_condition_is_equal = False
					if boolean_condition_is_equal and int(line[1].split(',')[1][2:],16)==0:
						boolean_condition_is_zero=True 
					temp_line=" % "+register_variable[last_register]+" == "+str(int(line[1].split(',')[1][2:],16))+")  {"+NEW_LINE
				elif register_values[register]==line[1].split(',')[1]:

					if register_values[register] == str(line[1].split(',')[1]):
						boolean_condition_is_equal = True
					else:
						boolean_condition_is_equal = False

					if boolean_condition_is_equal and int(line[1].split(',')[1])==0:
						boolean_condition_is_zero=True 
					temp_line=" % "+register_variable[last_register]+" == "+str(int(line[1].split(',')[1]))+")  {"+NEW_LINE

	elif line[0] == "JZ":
		jump_point=line[1]

		if boolean_condition_is_zero:
			is_jumping=True
		else:
			is_jumping=False
		C_PROGRAM=C_PROGRAM+TAB+"if ( "+temp_line


	elif line[0] == "JMP":
		jump_point=line[1]

		if boolean_condition_is_zero:
			is_jumping=True
		else:
			is_jumping=False

		if not is_branch_added:
			C_PROGRAM=C_PROGRAM+TAB+"else { "

	elif jump_point+":" == line[0]:
			print "here"
			is_jumping=False

	i = i+1

print "\n"

C_PROGRAM = C_PROGRAM+C_PROGRAM_END
print C_PROGRAM
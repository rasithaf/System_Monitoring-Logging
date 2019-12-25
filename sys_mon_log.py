#!/usr/bin/env python
#----------------------------------------------#
# Author: Rasitha Fernando---------------------#
# Last update: December 20, 2019---------------#
# only works for 4-core and 6-core systems-----#
# python 2.7-----------------------------------#
# Version 1.0----------------------------------#
#----------------------------------------------#

import os ,datetime, psutil
	
cpu_perc = psutil.cpu_percent(interval=1, percpu=True) #test for number of cores

name = 'sysmon_record.txt'
if os.path.isfile(name):
	print ("File already exists to update")
else:
	f= open(name,"w+")
	print ("File has been created to update")
	f.close()

core = len(cpu_perc)

if core == 4:
	L = ["Temp('C)	RAM (%)		Core1(%)	Core2(%)	Core3(%)	Core4(%)	Time"]
	print("System has 4 cores")

if core == 6: 
	L = ["Temp('C)	RAM (%)		Core1(%)	Core2(%)	Core3(%)	Core4(%)	Core5(%)	Core6(%)	Time"]
	print("System has 6 cores")

file1 = open(name,"w") 
file1.writelines(L) 
file1.close()


def main():

	mem_perc = 0 
	cpu_perc = 0 
	gap = "	"*2
	prevtemp = 21                

	try :
		while True:
			temp = open("/sys/class/thermal/thermal_zone0/temp").read().strip().lstrip('temperature :').rstrip(' C')
			temp = int(temp) / 1000.0

			if prevtemp > 20 and temp < 18 :
				temp = temp * 10
			prevtemp = temp


			cpu_perc = psutil.cpu_percent(interval=1, percpu=True)
			mem_perc = psutil.virtual_memory().percent
			s_time = datetime.datetime.now()

			print(s_time)
			print "CPU Temperature: " , temp, "'C"
			for i in range(core):
				print "CPU Core", str(i+1),":", str(cpu_perc[i]), "%"
				
			print "RAM: ", mem_perc, "%"
			print "-"*30
			
			# Log data into the text file
			file1 = open(name,"a")
			if core == 4:
				file1.write("\n" + str(temp) + gap + str(mem_perc) + gap + str(cpu_perc[0]) + gap + str(cpu_perc[1]) + gap + str(cpu_perc[2]) + gap + str(cpu_perc[3]) + gap + str(s_time)) 
			if core == 6:
				file1.write("\n" + str(temp) + gap + str(mem_perc) + gap + str(cpu_perc[0]) + gap + str(cpu_perc[1]) + gap + str(cpu_perc[2]) + gap + str(cpu_perc[3]) + gap + str(cpu_perc[4]) + gap + str(cpu_perc[5]) + gap + str(s_time)) 

			file1.close() 
             
	except KeyboardInterrupt :
		pass                 
		print("Log has been updated")   
		file1 = open(name,"a") 
		file1.write("\n")
		file1.writelines(L) 
		file1.close()              
                



if __name__ == '__main__':        
        main()


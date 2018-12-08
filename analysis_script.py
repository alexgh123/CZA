#==========================
# date:      11/26/2018
# author:    Alex
#
# question:  what kind of time based pattern is there w/ the data
#
#==========================

#input file format:
#2607:f8b0:4005:804::200e , google.com , 12.539 , 26/11/2018 00:00:05 UTC
#2001:4998:c:1023::4      , yahoo.com ,  32.822 , 26/11/2018 00:00:07 UTC


# ideal answer format:
# time| google.com | yahoo.com | aline.com | vatican.com |facebook.com| navycaptain-therealnavy.blogspot.com
#  ---+------------+-----------+-----------+-------------+------------+---------------
#   8 |  avg_time  |           |           |             |            |               
#   9 |            |           |           |             |            |               
#   10|            |           |           |             |            |               
#   11|            |           |           |             |            |               
#  
#              

#first dict we use has this format:
	#  {url1 :[hour_0_ping_1_time, hour_0_ping_2_time...], [hour_1_ping_1_time, hour_1_ping_2_time...] ...
    #   url2 : ....
    #   ....	
	#  }
	
	# {facebook: [[1, 2.2...],[1, 1.1, 3.2]...],
	#  url2    : [[1, 2.2...],[1, 1.1, 3.2]...],
	#  ....
	# }


# second dict will average each hourl_bin
'''
{'yahoo.com': 
	[62.067, 60.087, 61.468, 62.93, 61.216, 59.812, 61.798, 59.526, 62.396, 58.323, 59.557, 62.639, 59.079, 58.699, 62.78, 60.82, 55.046, 61.348, 59.913, 62.686, 59.072, 61.123, 63.783, 61.444], 
	    ^                                     ^
	    |average ping time from 0000-0100     |
	                                          |average ping time from 0500-0600


'''

import csv
from datetime import datetime

import matplotlib.pyplot as plt
import numpy as np

# num_bins = 2
seconds_in_an_hour = 3600
# num_failed_recs = 0

def Average(list):
	if((len(list))==0):
		# print("here is bad list:")
		# print(list)
		output = "no_pings"
	else:
		output = sum(list) / len(list) 
	return output


def analyzeFile(fileName):

	counter=0
	num_failed_recs = 0
	# limit_to_lines = 250
	dict_of_sites = {}

	with open(fileName) as csv_file:
		csv_reader = csv.reader(csv_file, delimiter=',')
	
		for line in csv_reader:
			counter += 1
			#don't use first three lines, its metadata
			if(counter<= 3):
				continue
			#break at limit for development purposes
			#if (counter >= limit_to_lines):
			#	break
			
			# need to get seconds since midnight for each row
			# so that I know which bin to put each rec in
			# data format 26/11/2018 00:00:05 UTC
			# some data is corrupted, so if below line fails, 
			# it means we don't have average ping time for it
			try:
				row_time = datetime.strptime(line[3], ' %d/%m/%Y %H:%M:%S %Z ')
			except:
				#if the above operation fails, we'll throw out the data
				num_failed_recs +=1
				# print("failed with this line:")
				# print(line)
				continue
			seconds_since_midnight = (row_time - row_time.replace(hour=0, minute=0, second=0, microsecond=0)).total_seconds()
			
			# below operation will provide correct index number to find correct 
			# hourly bin to store times in
			correct_bin_index = int(seconds_since_midnight/seconds_in_an_hour)
			
			#format some data...
			url = line[1].strip()
			try:
				ping_time = float(line[2].strip())
			except:
				num_failed_recs +=1
				continue

	
			#do dictionary check, if key in dict...
			# just add the record
			if(url in dict_of_sites):
				dict_of_sites[url][correct_bin_index].append(ping_time)
			#if key doesn't exist, create blank bins
			# add first time to correct bin
			else:
				bins = [[] for _ in range(24)]
				# print("dict doesn't have key, here is line[1]")
				# print(url)
				dict_of_sites[url]= bins
				dict_of_sites[url][correct_bin_index].append(ping_time)

	print("done analyzing this file:")
	print(fileName)
	print('this many exceptions:')
	print(num_failed_recs)
	return dict_of_sites

#at this point, we have the dictionary object
#    {url:[[],[]...]}
# for every ping time
#BUT we need average ping time for each hour!
# (below code does that)

def getAverageHourlyPing(dictInput):
	for url in dictInput:
		index_into_nested_list = 0
		for hourly_bin in dictInput[url]:
			
			#if(url == "google.com"):
			#	print(" ")
			#	print(" here! ")
			#	print(hourly_bin)
			#	print(" ")

			# if(len(hour))
			hourly_bin = Average(hourly_bin)
			#below line introduces dependency on our input file (specifically index number)
			# but its ok because our log files run all day, and midnight is the first
			# hour in the day
			if(hourly_bin=="no_pings"):
				avg = "no_pings"
			else:
				avg = round(hourly_bin, 3)
			dictInput[url][index_into_nested_list] = avg
			index_into_nested_list += 1
	return dictInput 

# file = "20181129_Z_outFile.txt"
# new_dict = analyzeFile(file)
# hourlyAverage = getAverageHourlyPing(new_dict)

# print("here is your dictionary of average ping time, hourly...")
# print(hourlyAverage)

# exit()

#get list of files
#iterate through them
# with open("list_of_files.txt") as f:
    # listOfFiles = f.readlines()
# listOfFiles = [x.strip() for x in listOfFiles] 
# print(listOfFiles)

# exit()

zaki_27 = ["20181127_Z_outFile.txt"]

alex_weekday_files = ["20181113_A_outFile.txt","20181114_A_outFile.txt","20181115_A_outFile.txt","20181116_A_outFile.txt","20181119_A_outFile.txt","20181120_A_outFile.txt","20181121_A_outFile.txt","20181126_A_outFile.txt","20181127_A_outFile.txt","20181128_A_outFile.txt","20181129_A_outFile.txt","20181130_A_outFile.txt"]

zaki_weekday_files = ["20181113_Z_outFile.txt","20181114_Z_outFile.txt","20181115_Z_outFile.txt","20181116_Z_outFile.txt","20181119_Z_outFile.txt","20181120_Z_outFile.txt","20181121_Z_outFile.txt","20181126_Z_outFile.txt","20181127_Z_outFile.txt","20181128_Z_outFile.txt","20181129_Z_outFile.txt","20181130_Z_outFile.txt"]

corey_weekday_files = ["20181113_C_outFile.txt","20181114_C_outFile.txt","20181115_C_outFile.txt","20181116_C_outFile.txt","20181119_C_outFile.txt","20181120_C_outFile.txt","20181121_C_outFile.txt","20181126_C_outFile.txt","20181127_C_outFile.txt","20181128_C_outFile.txt","20181129_C_outFile.txt","20181130_C_outFile.txt"]

all_weekday_files = alex_weekday_files + zaki_weekday_files+ corey_weekday_files

alex_weekend_files = ["20181111_A_outFile.txt", "20181112_A_outFile.txt","20181117_A_outFile.txt","20181118_A_outFile.txt","20181122_A_outFile.txt","20181123_A_outFile.txt","20181124_A_outFile.txt","20181125_A_outFile.txt"]

corey_weekend_files = ["20181111_C_outFile.txt", "20181112_C_outFile.txt","20181117_C_outFile.txt","20181118_C_outFile.txt","20181122_C_outFile.txt","20181123_C_outFile.txt","20181124_C_outFile.txt","20181125_C_outFile.txt"]

zaki_weekend_files = ["20181111_Z_outFile.txt", "20181112_Z_outFile.txt","20181117_Z_outFile.txt","20181118_Z_outFile.txt","20181122_Z_outFile.txt","20181123_Z_outFile.txt","20181124_Z_outFile.txt","20181125_Z_outFile.txt"]

all_weekend_files = zaki_weekend_files + alex_weekend_files +corey_weekend_files

all_files = all_weekend_files + all_weekday_files

all_alex_files = alex_weekday_files + alex_weekend_files
all_zaki_files = zaki_weekday_files + zaki_weekend_files
all_corey_files = corey_weekday_files + corey_weekend_files

c_a_weekend_files = alex_weekend_files +corey_weekend_files

files_list = all_zaki_files

allHourlyAverages = []
for file in files_list:
	new_dict = analyzeFile(file)
	hourlyAverage = getAverageHourlyPing(new_dict)
	# print(hourlyAverage)
	# print("this file:")
	# print(file)
	# print("generates this data:")
	# print(hourlyAverage)
	allHourlyAverages.append(hourlyAverage)



masterDict = {}
for hourlyAverage in allHourlyAverages:
	# print(" ")
	# print(" here is the hourly average we are going to work with:")
	# print(hourlyAverage)

	for site, hourlyBinsList in hourlyAverage.iteritems():
		indexIntoBin = 0
		for hourlyBin in hourlyBinsList:
			# print(" ")
			# print("old masterDict")
			# print(masterDict)

			# a = raw_input("press enter")
			
			#REMINDER: check if hourlyBin is int.....
			
			#masterDict =
				# yahoo.com: [
				#             [33,2]
				#             [44,2]
				#            ]

			#add hourlyBin Time to masterelement 0 to itself
			# masterDict[site]
				#returns [[a,1],[b,2],[c,3],[]]


			# {}


			if (hourlyBin == "no_pings"):
				indexIntoBin += 1
				continue
			else:
				if site in masterDict:
					# c = raw_input('here is your thingy')
					# print(masterDict[site][indexIntoBin])
					if(len(masterDict[site][indexIntoBin]) == 0):
						masterDict[site][indexIntoBin] = [hourlyBin,1]
					else:
						# print("old dict, pre update:")
						# print(masterDict)
						# c = raw_input('here is your thingy')
						masterDict[site][indexIntoBin][0] += hourlyBin
						masterDict[site][indexIntoBin][1] += 1
						# print(masterDict)
					# masterDict[site][indexIntoBin][1] += 1
				else:
					masterDict[site] = [[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[]]
					# print("here is master dict before update...")
					# print(masterDict)
					# b = raw_input("press enter")
					# print("here is masterDict at indexIntoBin")
					# print(masterDict[site][indexIntoBin])

					masterDict[site][indexIntoBin] = [hourlyBin,1]
					# masterDict[site][indexIntoBin][1].append(1)

			indexIntoBin += 1

		# print("new masterDict")
		# print(masterDict)
# print(masterDict)

for site, list_of_time_count_pairs in masterDict.iteritems():
	list_index = 0
	for pair in list_of_time_count_pairs:
		masterDict[site][list_index] = round((pair[0]/pair[1]), 2)
		list_index += 1

print(" ")
print(" average for these file:")
print(files_list)
print(" ")
print(masterDict)

print(" ")

# ax.bar(x-0.2, y,width=0.2,color='b',align='center')
# ax.bar(x, z,width=0.2,color='g',align='center')
# ax.bar(x+0.2, k,width=0.2,color='r',align='center')
# ax.xaxis_date()

colors = ["red", "blue", "green", "orange", "black", "yellow", "purple", "magenta"]
# ax = plt.subplot()
# x=1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23
i = 0

fig, ax, = plt.subplots()
# rects1 = ax.bar()

# for site, array_of_times in masterDict.iteritems():
y = masterDict["yahoo.com"]
g = masterDict["google.com"]
a = masterDict["aline.com"]
f = masterDict["facebook.com"]
n = masterDict["navycaptain-therealnavy.blogspot.com"]
v = masterDict["vatican.com"]
# r = masterDict["10.0.0.1"]



plt.plot(y, color=colors[0], label="yahoo.com",   linewidth=4)
# plt.plot(g, color=colors[1], label="google.com",  linewidth=4)
# plt.plot(a, color=colors[2], label="aline.com",   linewidth=4)
# plt.plot(f, color=colors[3], label="facebook.com",linewidth=4)
# plt.plot(n, color=colors[4], label="navycaptain-therealnavy.blogspot.com",linewidth=4)
plt.plot(v, color=colors[5], label="vatican.com", linewidth=4)
# plt.plot(r, color=colors[6], label="10.0.0.1",    linewidth=4)
fig.suptitle('Zaki Low Performers')

plt.xlabel('Hour of Day', fontsize=18)
plt.ylabel('Latency (ms)', fontsize=16)
plt.legend(loc='best')


plt.show()





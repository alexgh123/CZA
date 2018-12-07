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
with open("list_of_files.txt") as f:
    listOfFiles = f.readlines()
listOfFiles = [x.strip() for x in listOfFiles] 
# print(listOfFiles)

# exit()

allHourlyAverages = []
for file in listOfFiles:
	new_dict = analyzeFile(file)
	hourlyAverage = getAverageHourlyPing(new_dict)
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
print(masterDict)

for site, list_of_time_count_pairs in masterDict.iteritems():
	list_index = 0
	for pair in list_of_time_count_pairs:
		masterDict[site][list_index] = round((pair[0]/pair[1]), 2)
		list_index += 1

print(" ")
print(" average for these file:")
print(listOfFiles)
print(" ")
print(masterDict)

print(" ")

# ax.bar(x-0.2, y,width=0.2,color='b',align='center')
# ax.bar(x, z,width=0.2,color='g',align='center')
# ax.bar(x+0.2, k,width=0.2,color='r',align='center')
# ax.xaxis_date()

colors = ["red", "blue", "green", "orange", "black", "yellow", "purple"]
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

N = len(y)
width = 0.6
ind = np.arange(N)
fig, ax = plt.subplots()
w=.2

print(ind-width/6)
print(" ")
print(ind-width*2/6)
print(" ")
print(ind-width*3/6)
print(" ")
print(ind+width/6)
print(" ")
print(ind+width*2/6)
print(" ")
print(ind+width*3/6)
print(" ")
# exit()

ax.bar(ind-width/6,   y, width, align='center', color=colors[0], label="yahoo.com")
ax.bar(ind-width*2/6, g, width, align='center', color=colors[1], label="google.com")
ax.bar(ind-width*3/6, a, width, align='center', color=colors[2], label="aline.com")
ax.bar(ind+width/6,   f, width, align='center', color=colors[3], label="facebook.com")
ax.bar(ind+width*2/6, n, width, align='center', color=colors[4], label="navycaptain-therealnavy.blogspot.com")
ax.bar(ind+width*3/6, v, width, align='center', color=colors[5], label="vatican.com")
ax.autoscale(tight=True)

# y = masterDict["google.com"]
# rects1 = ax.bar(ind, y, width, color='g')

# for site, array_of_times in masterDict.iteritems():
	# y = array_of_times
	# x = range(N)

	# plt.subplot(x, y,width,color=colors[i],align='center')
	# plt.bar(x, y, width, color="blue")
	# i +=1

plt.show()
	# plt.bar(24,np.array(array_of_times), width, color='blue')

	# y = [3, 10, 7, 5, 3, 4.5, 6, 8.1]
	# N = len(y)
	# x = range(N)
	# width = 1/1.5
	# plt.bar(x, y, width, color="blue")
	#label each line
	#all on same plot



exit()
#if int
	# masterDict[site] = 
	#else not int

	# yahoo:     [[59, 3],[59, 3]]
	# aline.com: [22, 4]

'''
	{'yahoo.com': [no_pings, 'no_pings', 60.676, 59.458, 64.704, 63.389, 58.021, 58.023, 58.802, 58.637, 58.67, 59.693, 59.15, 59.427, 59.477, 58.634, 62.076, 60.102, 59.414, 60.593, 59.161, 59.757, 60.091, 59.572], 
	'aline.com': [15.218, 15.087, 15.56, 15.508, 20.739, 19.841, 15.201, 15.103, 14.386, 13.358, 13.37, 13.236, 14.088, 14.686, 14.736, 14.714, 15.26, 15.069, 14.909, 15.011, 14.879, 14.707, 14.883, 14.931],
	'google.com': [14.924, 15.145, 15.424, 15.187, 20.135, 19.87, 15.679, 14.885, 14.118, 13.35, 13.127, 13.209, 13.874, 14.681, 14.637, 15.337, 15.031, 15.076, 14.689, 14.819, 15.267, 15.306, 14.759, 14.738],
	'navycaptain-therealnavy.blogspot.com': [15.534, 15.243, 15.794, 15.785, 20.227, 19.515, 15.387, 15.037, 14.041, 13.424, 14.593, 13.303, 14.038, 14.933, 14.852, 14.82, 15.159, 15.052, 15.089, 14.967, 14.816, 14.772, 14.899, 14.847],
	'facebook.com': [15.235, 15.401, 16.008, 15.888, 20.534, 20.249, 15.182, 15.468, 14.53, 13.688, 13.557, 13.572, 14.298, 14.911, 15.044, 15.11, 15.326, 15.146, 15.121, 14.924, 15.241, 15.017, 15.05, 15.031], 
	'10.0.0.1': [2.156, 2.0, 2.016, 2.46, 2.035, 2.074, 2.854, 2.002, 2.001, 2.003, 2.021, 2.012, 2.003, 1.994, 2.113, 2.005, 2.828, 2.015, 2.019, 1.979, 2.015, 2.011, 1.998, 2.011], 
	'vatican.com': [59.347, 59.389, 60.056, 59.945, 64.366, 64.17, 59.401, 59.205, 58.675, 57.814, 57.91, 57.808, 58.612, 58.795, 59.138, 59.141, 59.304, 59.168, 59.136, 59.159, 59.036, 59.021, 59.284, 59.262]}

	{'yahoo.com': [59.233, 'no_pings', 60.676, 59.458, 64.704, 63.389, 58.021, 58.023, 58.802, 58.637, 58.67, 59.693, 59.15, 59.427, 59.477, 58.634, 62.076, 60.102, 59.414, 60.593, 59.161, 59.757, 60.091, 59.572], 
	'aline.com': [15.218, 15.087, 15.56, 15.508, 20.739, 19.841, 15.201, 15.103, 14.386, 13.358, 13.37, 13.236, 14.088, 14.686, 14.736, 14.714, 15.26, 15.069, 14.909, 15.011, 14.879, 14.707, 14.883, 14.931],
	 'google.com': [14.924, 15.145, 15.424, 15.187, 20.135, 19.87, 15.679, 14.885, 14.118, 13.35, 13.127, 13.209, 13.874, 14.681, 14.637, 15.337, 15.031, 15.076, 14.689, 14.819, 15.267, 15.306, 14.759, 14.738],
	 'navycaptain-therealnavy.blogspot.com': [15.534, 15.243, 15.794, 15.785, 20.227, 19.515, 15.387, 15.037, 14.041, 13.424, 14.593, 13.303, 14.038, 14.933, 14.852, 14.82, 15.159, 15.052, 15.089, 14.967, 14.816, 14.772, 14.899, 14.847],
	 'facebook.com': [15.235, 15.401, 16.008, 15.888, 20.534, 20.249, 15.182, 15.468, 14.53, 13.688, 13.557, 13.572, 14.298, 14.911, 15.044, 15.11, 15.326, 15.146, 15.121, 14.924, 15.241, 15.017, 15.05, 15.031], 
	'10.0.0.1': [2.156, 2.0, 2.016, 2.46, 2.035, 2.074, 2.854, 2.002, 2.001, 2.003, 2.021, 2.012, 2.003, 1.994, 2.113, 2.005, 2.828, 2.015, 2.019, 1.979, 2.015, 2.011, 1.998, 2.011], 
	'vatican.com': [59.347, 59.389, 60.056, 59.945, 64.366, 64.17, 59.401, 59.205, 58.675, 57.814, 57.91, 57.808, 58.612, 58.795, 59.138, 59.141, 59.304, 59.168, 59.136, 59.159, 59.036, 59.021, 59.284, 59.262]}
	'''
	#print(" ")
	#print(" ")





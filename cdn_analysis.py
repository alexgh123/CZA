import csv
from datetime import datetime

import matplotlib.pyplot as plt
import numpy as np

from sets import Set

# num_bins = 2
seconds_in_an_hour = 3600
# num_failed_recs = 0

unique_IPs = Set()


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
	dict_of_urls_to_IPS = {}

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
			
			#desired output:
			#{url: Set(IP1, IP2, IP3)}

			url = line[1].strip()
			
			if("(" in line[0]):
				ip = line[0].split("(")[1].strip()
				#split line
			else:
				ip  = line[0].strip()
			
			#print(" ")
			#print(line)
			#print(url)

			#print(ip)
			#print(len(ip))
			
			if(len(ip) < 3):
				continue
				# print(line)
				# print("here^")
				# exit()

			#print(" ")

			try:
				#if key exists
				if(url in dict_of_urls_to_IPS):
					#add IP to set
					dict_of_urls_to_IPS[url].add(ip)
					#if(url == "vatican.com"):
						#print(url)
						# print(ip)
						# print(dict_of_urls_to_IPS[url])
						# a = raw_input("press enter")
				#else key doesn't exist
				else:
					#add url, ip
					initial_set = Set()
					initial_set.add(ip)
					dict_of_urls_to_IPS[url] = initial_set
					#print(" ")
					#print(line)
					#print(ip)
					#print(dict_of_urls_to_IPS[url])
					#a = raw_input("press enter")
			except:
				num_failed_recs +=1
				continue

	print("done analyzing this file:")
	print(fileName)
	print('this many exceptions:')
	print(num_failed_recs)
	return dict_of_urls_to_IPS

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

bad_files = ["20181127_Z_outFile.txt", "20181127_A_outFile.txt", "20181127_C_outFile.txt"]
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

considered_url_ip = {"google.com": Set(),"yahoo.com": Set(),"aline.com": Set(),"vatican.com": Set(),"facebook.com": Set(),"navycaptain-therealnavy.blogspot.com": Set(),"10.0.0.1": Set()}

'''('yahoo.com', 6)
('aline.com', 2)
('google.com', 38)
('navycaptain-therealnavy.blogspot.com', 29)
('facebook.com', 2)
('10.0.0.1', 1)
('vatican.com', 1)'''

considered_files = ["20181130_Z_outFile.txt", "20181130_A_outFile.txt", "20181130_C_outFile.txt"]
for file in considered_files:
	new_dict = analyzeFile(file)
	print(" ")
	print("for this file:")
	print(file)
	print("new dict:")
	for url, ip_set in new_dict.iteritems():
		# print(url, len(ip_set))
		considered_url_ip[url] = considered_url_ip[url].union(ip_set)


print(" ")
print("for the analysis of these files:")
print(considered_files)
print(" ")
print("we have these URLs, with this many IPs")
for key, value in considered_url_ip.iteritems():
		print(key) 
		print(len(value))

exit()

# plt.boxplot(column=len(considered_url_ip.values()), by=considered_url_ip.keys())

# or backwards compatable    
labels, data = considered_url_ip.keys(), list(considered_url_ip.values())

plt.boxplot(data)
plt.xticks(range(1, len(labels) + 1), labels)
plt.show()

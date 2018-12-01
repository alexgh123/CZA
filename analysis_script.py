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

counter=0
limit_to_lines = 25000
second_counter = 0
dict_of_sites = {}

num_bins = 2
seconds_in_an_hour = 3600

def Average(list): 
    return sum(list) / len(list) 

with open('20181126_A_outFile.txt') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')

    for line in csv_reader:
		counter += 1
		#don't use first three lines, its metadata
		if(counter<= 3):
			continue
		#break at limit for development purposes
		if (counter >= limit_to_lines):
			break
		
		# need to get seconds since midnight for each row
		# so that I know which bin to put each rec in
		# data format 26/11/2018 00:00:05 UTC
		row_time = datetime.strptime(line[3], ' %d/%m/%Y %H:%M:%S %Z ')
		seconds_since_midnight = (row_time - row_time.replace(hour=0, minute=0, second=0, microsecond=0)).total_seconds()
		
		# below operation will provide correct index number to find correct 
		# hourly bin to store times in
		correct_bin_index = int(seconds_since_midnight/seconds_in_an_hour)
		
		#format some data...
		url = line[1].strip()
		ping_time = float(line[2].strip())

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

#at this point, we have the dictionary object
#    {url:[[],[]...]}
# for every ping time
#BUT we need average ping time for each hour!
# (below code does that)

new_dict = dict_of_sites
for url in new_dict:
	index_into_nested_list = 0
	for hourly_bin in new_dict[url]:
		hourly_bin = Average(hourly_bin)
		#below line introduces dependency on our input file (specifically index number)
		# but its ok because our log files run all day, and midnight is the first
		# hour in the day
		new_dict[url][index_into_nested_list] = round(hourly_bin, 3)
		index_into_nested_list += 1

# print("here is your dictionary of average ping time, hourly...")
# print(new_dict)


#write output somewhere productive:
	#googleFile
	#yahooFile
		# output to those files:
			# date:avg_for_that_day






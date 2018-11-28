#==========================
# date:      11/26/2018
# author:    Alex
#
# question:  what kind of time based pattern is there w/ the data
#
#==========================



# answer format:
# time| google.com | yahoo.com | aline.com | vatican.com |facebook.com| navycaptain-therealnavy.blogspot.com
#  ---+------------+-----------+-----------+-------------+------------+---------------
#   8 |  avg_time  |           |           |             |            |               
#   9 |            |           |           |             |            |               
#   10|            |           |           |             |            |               
#   11|            |           |           |             |            |               
#  
#              

#sites = {site: [count, total time]}
#         avg: time/count

#sites = {site: {num_hours: }}
		# site: {num_bins_starting_at_midnight: [avg_ping_time]}
		# we'll have an intermediate set where we have this:
		
		# {facebook: {1: [100, 200.2], 2: [100, 1.1, 3.2], 3: [...}
		
		# {facebook: [100, {1: 200, 2:220, }]
		
		# ^the 100 is the number of entries for that dict
		#final setup will be: 
		# {facebook: {1: [2.2], 2: [1.1, 3.2], 3: [...}
		#we need to track number of entries

# how do i get a configurable grain of the data?
#		#one argument, number of bins
#       user sets max number bins
#24/2

# biggest grain we have is by day
# we'll have a program that writes to intermediate file

#program arguments:
	# file_name, multiple files
	# grain you want analysis

#read in records
	#handle headers

	#how do we want to organize data?
		#what question am i asking?

#first step:
	# read one file, get average time
# follwing steps:
	# handle multiple files
	# create configurable argument to specify number of bins
		# what are day boundaries?!?!
		# we could have a "current grain" field when, once exceeded, creates a new bin
		#


#read in file, throw out first three lines
import csv
from datetime import datetime

# file = open("20181126_A_outFile.txt", "r")
counter=0
limit_to_lines = 15
second_counter = 0
dict_of_sites = {}

num_bins = 2
seconds_in_a_day = 86400
seconds_in_an_hour = 3600

# {
#   facebook: [[12.3, 2.2, 3.1], [AVG]],
#   2ndsite:  [[3.3, 20.2, 30.1], [avg]],
#
# }

#2607:f8b0:4005:804::200e , google.com , 12.539 , 26/11/2018 00:00:05 UTC  
#2001:4998:c:1023::4      , yahoo.com ,  32.822 , 26/11/2018 00:00:07 UTC  





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
		#format 26/11/2018 00:00:05 UTC
		row_time = datetime.strptime(line[3], ' %d/%m/%Y %H:%M:%S %Z ')
		seconds_since_midnight = (row_time - row_time.replace(hour=0, minute=0, second=0, microsecond=0)).total_seconds()
		correct_bin_index = int(seconds_since_midnight/seconds_in_an_hour)
		url = line[1].strip()
		ping_time = float(line[2].strip())


		#do dictionary check, if key in dict...
		print(" ")
		print("examining this line:")
		print(line)
		if(url in dict_of_sites):
			#something
			print("dict has key...")
			dict_of_sites[url][correct_bin_index].append(ping_time)
		#populate dict w/ new bin if doesn't exist
		else:
			bins = [[] for _ in range(24)]
			print("dict doesn't have key, here is line[1]")
			print(url)
			dict_of_sites[url]= bins
			dict_of_sites[url][correct_bin_index].append(ping_time)

		print(dict_of_sites)

		print(" ")
		check = raw_input("press_enter")
		print(" ")

		#examine number of seconds, place time in appropriate bin

		# get average time for each bin
		# if()
		
		# print(line[1])

# print(dict_of_sites)
	






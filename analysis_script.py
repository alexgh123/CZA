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
		#{facebook: {1: [2.2], 2: [1.1, 3.2]}}

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

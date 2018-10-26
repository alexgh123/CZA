

NUM_PINGS=5
ARRAY_OF_HOSTS=("google.com", "netflix.com", "three")
PING_OUTPUT_FILE="outFile.txt"


#specs:
	#desired output:
		# 1. send several pings
		# 1.1 results from pings
		# 2. need a timestamp

#1.find default gateway 
DEF_GATE_WAY_STRING="$(route get default | grep gateway | cut -d':' -f 2)"
# echo"x"
#echo "$DEF_GATE_WAY_STRING"

HOST="googsssssssle.com"

#what does this line of code mean?
#   #1>/dev/null 2>/dev/null
# send std_error (2) to /dev/null
# send std_output(1) to /dev/nul
# a failed ping will only write to outfile if we pipe #2 as seen below

ping -c1 $HOST 1>"$PING_OUTPUT_FILE" 2>"$PING_OUTPUT_FILE"
SUCCESS=$?

if [ $SUCCESS -eq 0 ]
then
   echo "$HOST has replied, proceeding to ping"

else
  echo "$HOST didn't reply"
fi



#EOF

#DONE # check for success of gateway ping
	# if ping gateway success, 
		# record successful gateway ping
		# ping list of hosts
			#use average of 2-5 pings 
				#ping -c 5 url
			#write output of each ping to file
				#specifically 
					# TOD (time of day)
					# HOST (Gateway or IP_ADDR from urls_to_ping)
					# ping stats (average roundtrip time of pings)
				# how to write
					# echo "statss" >> ping_file_start_date_time
	# else (no ping success)
		#insert FAILED_TO_PING_GATEWAY into PING_FILE.txt

	# sleep 10 mins

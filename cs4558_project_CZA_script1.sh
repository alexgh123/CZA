

NUM_PINGS=5
# urls_to_ping = []

#specs:
	#desired output:
		# 1. send several pings
		# 1.1 results from pings
		# 2. need a timestamp

#1.find default gateway 
DEF_GATE_WAY_STRING="$(route get default | grep gateway | cut -d':' -f 2)"
# echo"x"
#echo "$DEF_GATE_WAY_STRING"

HOST=$DEF_GATE_WAY_STRING

ping -c1 $HOST #1>/dev/null 2>/dev/null
SUCCESS=$?

if [ $SUCCESS -eq 0 ]
then
  echo "$HOST has replied"
else
  echo "$HOST didn't reply"
fi
#EOF

# check for success of gateway ping
	# if ping gateway success, 
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

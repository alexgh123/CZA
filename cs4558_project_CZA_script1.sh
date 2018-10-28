#!/bin/bash


# fields:
# ip, avg_time of 5 pings, tod

#ip, url, avg_time_of_NUM_PINGS, tod

NUM_PINGS=3
ARRAY_OF_HOSTS=("google.com" "yahoo.com" "netflix.com") #
PING_OUTPUT_FILE="outFile.txt"

DATE_TIME=$(date '+%d/%m/%Y %H:%M:%S');
echo "script starting at $DATE_TIME"> "$PING_OUTPUT_FILE"
echo "from this device:" >> "$PING_OUTPUT_FILE"
id >> "$PING_OUTPUT_FILE"

#specs:
	#desired output:
		# 1. send several pings
		# 1.1 results from pings
		# 2. need a timestamp

#1.find default gateway 
DEF_GATE_WAY_STRING="$(route get default | grep gateway | cut -d':' -f 2)"
# echo"x"
#echo "$DEF_GATE_WAY_STRING"

HOST="$DEF_GATE_WAY_STRING"
# HOST="googsssssssle.com"

#what does this (below) line of code mean?
#   #<some_preceeding_command>...1>/dev/null 2>/dev/null
# send std_error (2) to /dev/null
# send std_output(1) to /dev/nul
# a failed ping will only write to outfile if we pipe #2 as seen below

ping -c 1 $HOST 1>>"$PING_OUTPUT_FILE" 2>>"$PING_OUTPUT_FILE"
SUCCESS=$?

echo " " >> "$PING_OUTPUT_FILE"
echo "begining pings of hosts" >> "$PING_OUTPUT_FILE"
echo " " >> "$PING_OUTPUT_FILE"

if [ $SUCCESS -eq 0 ]
then
    echo "$HOST has replied, proceeding to ping list of hosts"
    
    for i in "${ARRAY_OF_HOSTS[@]}"
    do

    	OUTPUT=""
    	#foo="$foo World"

    	#we want actual time ping sent, so we reinvoke the method
    	DATE_TIME1=$(date '+%d/%m/%Y %H:%M:%S');

        PING_RESULT="$(ping -c $NUM_PINGS $i)"
    	SUCCESS=$?
    	AVG_TIME_OF_PINGS=$(echo "$PING_RESULT" | tail -1| awk '{print $4}' | cut -d '/' -f 2)
  
    	#https://stackoverflow.com/questions/9634915/extract-average-time-from-ping-c
    	# ping -c 4 www.stackoverflow.com | tail -1| awk '{print $4}' | cut -d '/' -f 2

    	#i want to run ping
        #          check for success
        #          parse string


		#i need to pipe output to thing
		# DEF_GATE_WAY_STRING="$(route get default | grep gateway | cut -d':' -f 2)"

		# PING_RESULT="$(ping -c $NUM_PINGS $i 1>>"$PING_OUTPUT_FILE" 2>>"$PING_OUTPUT_FILE")"
        # ping -c $NUM_PINGS $i 1>>"$PING_OUTPUT_FILE" 2>>"$PING_OUTPUT_FILE"

        # echo " "
       	# echo " 00000000000 " 
       	# echo " "
        
        # echo "here \/  (avg time, ip)"
        # echo "$AVG_TIME_OF_PINGS"

        # echo " "
       	# echo " 11111111111 " 
       	# echo " "

        # echo "$PING_RESULT"


        # echo "$i"
        # echo "$SUCCESS"
        # ping -c "$NUM_PINGS" $i | tail -1| awk '{print $4}' | cut -d '/' -f 2
       
       	# echo " "
       	# echo " 22222222222 " 
       	# echo " "


        # PING_RESULT1="$(ping -c $NUM_PINGS $i | cut -d'=' -f 2)"
        
        #foo="$foo World"
       # PING_RESULT="$(ping -c $NUM_PINGS $i)"
       # AVG_TIME_OF_PINGS=$(echo "$PING_RESULT" | tail -1| awk '{print $4}' | cut -d '/' -f 2)
        
        #https://unix.stackexchange.com/questions/307895/pulling-ip-address-from-ping-command-with-sed
        IP_OF_HOST="$(echo "$PING_RESULT" | sed -nE 's/^PING[^(]+\(([^)]+)\).*/\1/p')"



        OUTPUT="$IP_OF_HOST , $i , $AVG_TIME_OF_PINGS , $DATE_TIME "
        echo "$OUTPUT ">> "$PING_OUTPUT_FILE"

        echo " "
        echo "here is output variable: "
        echo "$OUTPUT"
        echo " "


        
        # echo "ping sent at $DATE_TIME" >> "$PING_OUTPUT_FILE"
        #for formatting
        #echo "success code:" >> "$PING_OUTPUT_FILE"
        #echo "$SUCCESS" >> "$PING_OUTPUT_FILE"

        if [ $SUCCESS -eq 0 ] ; then
        	echo "successful ping"
        else
        	echo "failed ping"
        	#problem, a failed ping hangs
        	#other stuff
        fi
        

    done
    #echo "out of ARRAY_OF_HOSTS loop"


else
  echo "$HOST didn't reply"
fi



#EOF

#DONE # check for success of gateway ping
	# if ping gateway success, 
		#DONE # record successful gateway ping in log file

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

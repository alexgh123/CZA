#!/bin/bash


# fields:
# ip, avg_time of 5 pings, tod

#ip, url, avg_time_of_NUM_PINGS, tod

HOST="$(ip route | grep default | cut -d " " -f 3)"

NUM_PINGS=3
ARRAY_OF_HOSTS=("$HOST" "google.com" "yahoo.com" "netflix.com") #
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


while(true)
do
    #loop


    #1.find default gateway 
    # HOST="$(ip route | grep default | cut -d " " -f 3)"
    
    # ping -c 1 $HOST 
    # SUCCESS=$?
    
    
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
          
            #https://unix.stackexchange.com/questions/307895/pulling-ip-address-from-ping-command-with-sed
            IP_OF_HOST="$(echo "$PING_RESULT" | sed -nE 's/^PING[^(]+\(([^)]+)\).*/\1/p')"
    
    
    
            OUTPUT="$IP_OF_HOST , $i , $AVG_TIME_OF_PINGS , $DATE_TIME "
            echo "$OUTPUT ">> "$PING_OUTPUT_FILE"
    
            echo " "
            echo "here is output variable: "
            echo "$OUTPUT"
            echo " "
    
    
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

    #sleep
    sleep 10 #seconds
done


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

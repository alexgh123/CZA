#specs:
	#desired output:
		# 1. send several pings
		# 1.1 results from pings
		# 2. need a timestamp

#1.find default gateway 
DEF_GATE_WAY_STRING="$(route get default | grep gateway | cut -d':' -f 2)"
# echo"x"
echo "$DEF_GATE_WAY_STRING"

ping $DEF_GATE_WAY_STRING

#stop pings



#2 record data received

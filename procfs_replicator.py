#!/usr/bin/python
#
# Copyright (c) 2018 [n/a] info@embeddora.com All rights reserved
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#        * Redistributions of source code must retain the above copyright
#          notice, this list of conditions and the following disclaimer.
#        * Redistributions in binary form must reproduce the above copyright
#          notice, this list of conditions and the following disclaimer in the
#          documentation and/or other materials provided with the distribution.
#        * Neither the name of The Linux Foundation nor
#          the names of its contributors may be used to endorse or promote
#          products derived from this software without specific prior written
#          permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NON-INFRINGEMENT ARE DISCLAIMED.    IN NO EVENT SHALL THE COPYRIGHT OWNER OR
# CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL,
# EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO,
# PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS;
# OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY,
# WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR
# OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF
# ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#
# Abstract:          a script top produce (partial) replica of RAM's/CUS's '/proc' 
#                    direcotry in local '/tmp/proc' (and its '/sys' replica in in
#                    local '/tmp/s@s'). 
#
# Usage:             not for standalone usage, has to be called from 'launcher.sh'
#                    instead.
#
# Version:           1.0


# Variable devnull
import os

# Function call (["", "", ""])
from subprocess import call



# PROGRAM ENTRY POINT

# Destination to redirect STDOUT and STDERR output to
devnull = open(os.devnull, 'w')

# Prepare a command to remove local mirror folder (presumably) created recently
cmd = "rm -rf /tmp/proc"

# Execute a command, disragard its output
result = os.popen(cmd).read()

# Prepare a command to remove local mirror folder (presumably) created recently
cmd = "rm -rf /tmp/sys"  

# Execute a command, disragard its output
result = os.popen(cmd).read()

# Prepare a command to prepare a root of local mirror folder
cmd = "mkdir -p /tmp/proc"

# Execute a command, disragard its output
result = os.popen(cmd).read()

# Prepare a command to prepare a root of local mirror folder
cmd = "mkdir -p /tmp/sys"  

# Execute a command, disragard its output
result = os.popen(cmd).read()

# Program main loop
while True:

	# Each time we start a cycle empty thet list of output strings
	allsymbs = ""

	# Process-ID strings (same are names of process subfolders in '/proc') are made '1..9' digits
	for D in ["1", "2", "3", "4", "5", "6", "7", "8", "9"]:

		# Prepare a command to list local (mirror) folders in truncated form
		cmd = "ssh root_nopass@192.168.88.179 'ls -d  /proc/" + D + "* 2>/dev/null ' "

		# Execute a command on Android peer and attach captured output to a list
		allsymbs += os.popen(cmd).read()




	# Prepare a command to list local (mirror) folders in truncated form
	cmd = "ls -1 -d  /tmp/proc/*/ | xargs -n1 basename" # TODO: get rid of 'basename: missing operand'



	# Capure the list of them into 'allsymbsLOCAL' while running a command
	allsymbsLOCAL = os.popen(cmd).read()


	# For each process number found in local mirror folder
	for Y in allsymbsLOCAL.split():

		# Form a substring like '/proc/Process-ID'
		Y1 = "/proc/" + Y

		# Check if this substring could not be found amoung those received from Android peer 
		if Y1 not in allsymbs:

			# Prepare folder erasure command - we don't need to mirror folders which don't exist on Android anymore 
			cmd = "rm -rf   /tmp/proc/" + Y

			# Exec. the cmd. withou output suppression (the command's should run smoothly, give us a feedbackl if not)
			specific_symbs = os.popen(cmd).read()



	# For each process number found on Android peer
	for X in allsymbs.split():

		# Create a mirror folder for current process 
		cmd = "mkdir -p /tmp" + str(X) 

		# Execute a command
		result = os.popen(cmd).read()

		# Create a mirror folder for 'net/dev'
		cmd = "mkdir -p /tmp/proc/net"

		# Execute a command
		result = os.popen(cmd).read()


		# Prepare common statistics files (to pass the initial check of 'launcher.sh')
		for Z in ["/loadavg", "/vmstat", "/stat", "/meminfo", "/1/task/1/cmdline"]:

			# Prepare command to feed c. statistics file with output suppression
			cmd = "ssh root_nopass@192.168.88.179 'cat  /proc"  + str(Z) + "' > /tmp/proc" + str(Z)

			# Execute a command
			result = os.popen(cmd).read()	


		# Prepare a command to create a directory (with parents) for command line entry of current process
		cmd = "mkdir -p /tmp" + str(X) + "/task/" + X.replace("/proc/",'')

		# Execute a command
		result = os.popen(cmd).read()



		# Prepare a command to feed command line for current process. (TODO: avoid '/1/task/1/cmdline' duplication)
		cmd = "ssh root_nopass@192.168.88.179 'cat " + str(X) + "/task/" + X.replace("/proc/",'') + "/cmdline'" + " > /tmp" + str(X)  + "/task/" + X.replace("/proc/",'') + "/cmdline"

		# Execute a command
		result = os.popen(cmd).read()



		# Prepare per-process statistics files (produce 'em: find . -maxdepth 1 -type f)
		for Y in ["/status","/cmdline","/stat","/statm" ]:

			# Prepare a command to feed per-process statistics file with output suppression
			cmd = "ssh root_nopass@192.168.88.179 'cat  " + str(X) + str(Y) + "' > /tmp" + str(X) + str(Y)

			# Execute a command
			result = os.popen(cmd).read()



		# Prepare common statistics files
		"""for Z in ["/cpuinfo", "/swaps", "/pagetypeinfo", "/modules", "/misc"]:

			# Prepare command to feed c. statistics file with output suppression
			cmd = "ssh root_nopass@192.168.88.179 'cat   /proc"  + str(Z) + "' > /tmp/proc" + str(Z)

			# Execute a command
			result = os.popen(cmd).read()"""



		# Prepare a comand to TODO: explain 
		"""cmd = "ssh root_nopass@192.168.88.179 'cat /proc/net/dev'" + " > /proc/net/dev"

		# Execute a command
		result = os.popen(cmd).read()

		# For each process number found on Android peer. # TODO: parse these values out of a 'proc/net/dev' 
		for K in ["lan0", "lo", "tiq0", "wan0"]:

			# Create a mirror folder for current process 
			cmd = "mkdir -p /tmp/sys/class/net/" + str(K)  + "/statistics/"

			# Execute a command
			result = os.popen(cmd).read()

			# For each process number found on Android peer			
			for L in ["rx_packets", "tx_packets", "rx_bytes", "tx_bytes", "rx_errors", "tx_errors", "collisions"]:

				# Prepare a cooamd to feed 'status' of current process 
				cmd = "ssh root_nopass@192.168.88.179 'cat /sys/class/net/" + str(K) + "/statistics/" + str(L) + "' > /tmp/sys/class/net/" + str(K) + "/statistics/" + str(L)

				# Execute a command
				result = os.popen(cmd).read()"""


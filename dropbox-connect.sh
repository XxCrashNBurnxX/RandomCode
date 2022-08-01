#!/bin/bash
# Run on Macbook to automate connection to a dropbox through pivot server (celestia)

#First get user input to select their dropbox
printf "Enter your dropbox-id? (i.e., 00123-1): "
read connection_id

if [ -z "$connection_id" ]; then
	print "Please enter a dropbox-id."
	exit 0
fi


#Check that the script user can access celestia with a{connection_id}
access="$(ssh a${connection_id}@66.109.142.165 dropbox-status)"

if [[ "$access" == *"denied"* ]]; then
	print "Permission denied for this dropbox, contact IT."
elif [[ "$access" == *"closed"* ]]; then
	print "Connection closed, please try again. Could be a network issue."
elif [[ "$access" == *"not connected"* ]]; then
	print "You have access, but dropbox is not currently connected."
elif [[ "$access" == *"is connected"* ]]; then
	#Kill bound ports on celestia for this user 
	processes="for pid in $(ps aux | grep ssh | grep a${connection_id} | grep -E 'D|L' | awk -F ' ' '{print $2}'); do kill ${pid}; done"
	ssh -q a${connection_id}@66.109.142.165 "${processes}"

	#Put connected port from celestia based on engagement number into variable
	connected_port="$(echo $access | awk '{print $6}')"
	socks_proxy="$((connected_port + 1))"
	scp_port="$((connected_port + 2))"

	#Kill local tmux windows to avoid conflict
	tmux kill-window -t scp > /dev/null 2>&1
	tmux kill-window -t socks > /dev/null 2>&1
	tmux kill-window -t gui > /dev/null 2>&1

	# create tmux windows
	tmux new-session -d -s scp
	tmux new-session -d -s socks
	tmux new-session -d -s gui

	#print readme documentation for the consultant to reference:
	printf "###########  READ ME  ###########
This script will create 3 ssh sessions using TMUX on your local MacBook.
  - socks:
  	Proxy your traffic through 127.0.0.1:3000
  - scp:
  	scp -P 3100 -r root@localhost:<REMOTE PATH TO COPY FROM> <LOCAL PATH TO COPY TO>
  - gui:
  	Use x2goclient to connect to full desktop environment via 127.0.0.1:2222 and XFCE desktop
###########  READ ME  ###########\n\n"

	#get user's public ssh key to allow GUI and SCP connections
	user_id_rsa="$(cat ~/.ssh/id_rsa.pub)"
	user_id_rsa_comment="$(echo $user_id_rsa | awk '{print $3}')"

	#Add user's public key to dropbox if not already on there (this only works if they are allowed to access the dropbox user on celestia, so it is pre-approved)
	key_added="$(ssh a${connection_id}@66.109.142.165 "ssh -q root@localhost -i /home/a${connection_id}/.ssh/id_rsa -p ${connected_port} 'grep $user_id_rsa_comment /root/.ssh/authorized_keys'")"
	if [ -z "$key_added" ]; then
		ssh a${connection_id}@66.109.142.165 "ssh -q root@localhost -i /home/a${connection_id}/.ssh/id_rsa -p ${connected_port} 'echo $user_id_rsa >> /root/.ssh/authorized_keys'"
	fi

	#connect 2 screen sessions and then standard shell 
	tmux send-keys -t socks "ssh -t -L 3000:localhost:${socks_proxy} a${connection_id}@66.109.142.165 ssh -q -D ${socks_proxy} root@localhost -i /home/a${connection_id}/.ssh/id_rsa -p ${connected_port}" ENTER
	tmux send-keys -t scp "ssh -t -L 3100:localhost:${scp_port} a${connection_id}@66.109.142.165 ssh -q -L ${scp_port}:localhost:22 root@localhost -i /home/a${connection_id}/.ssh/id_rsa -p ${connected_port}" ENTER
	tmux send-keys -t gui "ssh -o 'Compression=no' -L 2222:localhost:${connected_port} a${connection_id}@66.109.142.165" ENTER
	
	#connect to a standard shell
	ssh -t a${connection_id}@66.109.142.165 ssh -q root@localhost -i /home/a${connection_id}/.ssh/id_rsa -p ${connected_port}

	#After exiting main window, kill local tmux windows
	tmux kill-window -t scp > /dev/null 2>&1
	tmux kill-window -t socks > /dev/null 2>&1
	tmux kill-window -t gui > /dev/null 2>&1
fi

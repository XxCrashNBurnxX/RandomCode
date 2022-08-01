#!/bin/bash

#EXPECTED_ARGS=3
#E_BADARGS=127

#if [ $# -ne $EXPECTED_ARGS ]
#then
#    echo "This program takes $EXPECTED_ARGS arguments: the output filename, the address list filename, and the average RTT packet value."
#  echo "Usage: `basename $0` {arg} {arg} {arg}"
#  exit $E_BADARGS
#fi

CURRENTDATE="`date +'%Y_%m_%d-%H_%M_%S'`"
NUM=
output_filename=
address_list=
MAXNUM=
MINNUM=
scan_speed=4
extra_flags=


parse_syn(){
	grep -v ^# ${output_filename}_SYN_FULL.gnmap | sed 's/Ports: /\'$'\n/g' | tr '/' '\t' | tr ',' '\n' | sed 's/^ //g' | grep -v "Status: Up" | sed 's/Ignored State.*$//' | sed 's/Host/\'$'\n&/g' > ${output_filename}_SYN_FULL_parsed.txt
}
service_count_syn(){
	grep "/tcp.*open" ${output_filename}_SYN_FULL.nmap | awk '{print $3}' | sort | uniq -c > ${output_filename}_SYN_FULL_service_count.nmap
}
service_plus_version_count_syn(){
	grep "/tcp.*open" ${output_filename}_SYN_FULL.nmap | awk '{printf "%s %s %s %s\n", $3, $4, $5, $6}' | sort | uniq -c > ${output_filename}_SYN_FULL_service_plus_version.txt
}

parse_udp(){
	grep "/udp.*open" ${output_filename}_UDP_FULL.nmap > ${output_filename}_UDP_FULL_parsed.txt
}

service_count_udp(){
	grep "/udp.*open" ${output_filename}_UDP_FULL.nmap | awk '{print $3}' | sort | uniq -c > ${output_filename}_UDP_FULL_service_count.nmap
}
service_plus_version_count_udp(){
	grep "/tcp.*open" ${output_filename}_UDP_FULL.nmap | awk '{printf "%s %s %s %s\n", $3, $4, $5, $6}' | sort | uniq -c > ${output_filename}_UDP_FULL_service_plus_version.txt
}

parse_Syn_Full(){
	if [ ! -f ./${output_filename}_SYN_FULL.nmap ] 
		then
			echo "${output_filename}_SYN_FULL.nmap not found. Parsing skipped."
		else
			parse_syn
			service_count_syn
			service_plus_version_count_syn
	fi

	}
parse_Udp_Full(){
	if [ ! -f ./${output_filename}_UDP_FULL.nmap ] 
		then
			echo "${output_filename}_UDP_FULL.nmap not found. Parsing skipped."
		else
			parse_udp
			service_count_udp
			service_plus_version_count_udp
	fi
	}

SYN(){
echo "Starting SYN scan..."
#Standard SYN scan, default ports:
nmap --stats-every 10m -sS -A -PN -oA ${output_filename}_SYN -iL $address_list --max-rtt-timeout ${MAXNUM}ms --initial-rtt-timeout ${NUM}ms --min-rtt-timeout ${MINNUM}ms -T${scan_speed} $extra_flags
}

SYN_FULL(){
echo "Starting FULL SYN scan..."
#Standard SYN scan, all ports:
nmap --stats-every 10m -sS -A -PN -p 1-65535 -oA ${output_filename}_SYN_FULL -iL $address_list --max-rtt-timeout ${MAXNUM}ms --initial-rtt-timeout ${NUM}ms --min-rtt-timeout ${MINNUM}ms -T${scan_speed} $extra_flags
}

EGRESS_TEST(){
echo "Starting Egress Test..."
#Checks for all open ports outbound:
nmap egress.lmgsecurity.com -p- -oN ${output_filename}_Egress_Test
}

UDP(){
echo "Starting UDP scan..."
#Standard UDP scan, default ports:
nmap --stats-every 10m -sU -sV -oA ${output_filename}_UDP -iL $address_list --max-rtt-timeout ${MAXNUM}ms --initial-rtt-timeout ${NUM}ms --min-rtt-timeout ${MINNUM}ms --max-retries 3 -T${scan_speed} --host-timeout 6h $extra_flags
}

UDP_FULL(){
echo "Starting FULL UDP scan..."
#Standard UDP scan, all ports (ONLY do this if the first UDP scan didn't take a million years):
nmap  --stats-every 10m -sU -sV -p 1-65535 -oA ${output_filename}_UDP_FULL -iL $address_list --max-rtt-timeout ${MAXNUM}ms --initial-rtt-timeout ${NUM}ms --min-rtt-timeout ${MINNUM}ms --max-retries 3 -T${scan_speed} --host-timeout 6h $extra_flags
}

ACK_FULL(){
echo "Starting FULL ACK scan..."
#Full TCP ACK Scan (good for detecting firewall config:
nmap --stats-every 10m -sA -sV -PN -p 1-65535 -oA ${output_filename}_ACK_FULL -iL $address_list --max-rtt-timeout ${MAXNUM}ms --initial-rtt-timeout ${NUM}ms --min-rtt-timeout ${MINNUM}ms --max-retries 3 -T${scan_speed} --host-timeout 6h $extra_flags
}

FULL_SCAN(){
	printf "#################### STARTING FULL SCAN ####################\n\n"
	SYN
	SYN_FULL
	parse_Syn_Full
	UDP
	UDP_FULL
	parse_Udp_Full
	ACK_FULL
		OPTIND=8
}

DISCO_SCAN(){
	pingfilename=${output_filename}_PING_DISC.gnmap
	synfilename=${output_filename}_SYN_DISC.gnmap
	 
	#Scan 1: Ping Sweep Scan
	printf "#################### STARTING DISCO SCAN ####################\n\n"
	echo "Starting Ping Sweep..."
	nmap -sn -oA ${output_filename}_PING_DISC -iL $address_list --max-rtt-timeout ${MAXNUM}ms --initial-rtt-timeout ${NUM}ms --min-rtt-timeout ${MINNUM}ms -T${scan_speed} $extra_flags 
	 
	grep "Status: Up" $pingfilename  | awk '{print $2}' >> ${output_filename}_live_PING_DISC.txt
	 
	#Scan 2: SYN scan of 1000 ports treating all hosts as live, and attempting to fingerprint each OS
	echo "Starting default SYN scan of top 1000 ports"
	nmap --stats-every 10m -sS -O -PN -oA ${output_filename}_SYN_DISC -iL $address_list --max-rtt-timeout ${MAXNUM}ms --initial-rtt-timeout ${NUM}ms --min-rtt-timeout ${MINNUM}ms -T${scan_speed} $extra_flags 
	 
	grep '/open/tcp' $synfilename | awk '{print $2}' >> ${output_filename}_live_SYN_DISC.txt
	 
	echo "Analyzing results..."
	cat ${output_filename}_live_SYN_DISC.txt ${output_filename}_live_PING_DISC.txt | sort -u > ${output_filename}_live_IPs.txt
	 
	echo Discovery scanning is complete. List of live hosts located in:  ${output_filename}_live_IPs.txt
		OPTIND=8
}


usage (){
cat<<"EOT"

######################################################################
This script is used to run NMAP scans for the 1337 team.

COMMAND:
nmap-script.sh -n 20 -s 1234 -f <IP Address List> -o <output file> -x -g (optional)

OPTIONS:
-h Show this message
-m Use scan menu
-t scan speed (0-5)
   - default is 4
-e add extra flags
	-e "--excludefile filname"
-s Set scan sequence. Enter numbers in order you would like the scans to run
   - 1 (Default Syn)
   - 2 (Syn Full)
   - 3 (Default UDP)
   - 4 (UDP FULL)
   - 5 (Ack Full)
   - 6 (Egress)
   - 7 (Discovery)
-n RTT time
-o Output file name
-f Path to IP list file
-x Run full (1-5) Nmap scans (SYN,SYN_FULL,UDP,UDP_FULL,ACK_FULL).
-d Run discovery scan.
-g Run Egress Test.

EOT
}

parse_scan_sequence(){
	option=$1
	for i in $(seq 1 ${#option})
		do
			current_option=$(echo $option | cut -c$i)
			case $current_option in
				1)
					SYN
					;;
				2)
					SYN_FULL
					parse_Syn_Full
					;;
				3)
					UDP
					;;
				4)
					UDP_FULL
					parse_Udp_Full
					;;
				5)
					ACK_FULL
					;;
				6)
					EGRESS_TEST
					;;
				7)
					disco_art
					printf "Starting DISCO SCAN\n"
					DISCO_SCAN
					;;
				8) 
					exit 0
					;;
				?)
					echo invalid argument
					;;
			esac
		done
	}


menu(){
	while :
	do
		printf "#################### 1337 NMAP SCRIPT ####################\n\n"
		printf "Please select one or more of the following\n(for more than one option, enter the numbers in the order you would like the scans to run i.e. 12 for SYN then SYN FULL):\n\n1: SYN\n2: SYN FULL\n3: UDP\n4: UDP FULL\n5: ACK FULL\n6: EGRESS TEST\n7: DISCO SCAN\n8: Exit\n"
		read option
		parse_scan_sequence $option
		done
}

while getopts "hme:t:s:n:o:f:xdg" FLAG
do
	case $FLAG in 
		h)
			usage
			exit 1
			;;
		m)
			menu
			;;
		e)
			extra_flags=$OPTARG
			;;
		t)
			scan_speed=$OPTARG
			;;
		s)
			parse_scan_sequence $OPTARG
			;;
		n)
			NUM=$OPTARG
			MAXNUM=$(($NUM * 2)) 
			MINNUM=$(($NUM / 2)) 
			;;
		o)
			output_filename=$(printf "%s_%s" $OPTARG $CURRENTDATE)
			;;
		f)
			address_list=$OPTARG
			;;
		x)
			FULL_SCAN
			;;
		d)
			DISCO_SCAN
			;;
		g)
			EGRESS_TEST
exit 0
;;

	esac
done

#checks if the required parameters RTT, output filename and path to IP address list are present
if [[ -z $NUM ]] || [[ -z  $output_filename ]] || [[ -z $address_list ]]
then
	usage
	exit 1
fi

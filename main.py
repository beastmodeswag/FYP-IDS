import socket
import struct
import textwrap

from flask import Flask
from flask import render_template

TAB_1 = '\t - '
TAB_2 = '\t\t - '
TAB_3 = '\t\t\t - '
TAB_4 = '\t\t\t\t - '

DATA_TAB_1 = '\t '
DATA_TAB_2 = '\t\t '
DATA_TAB_3 = '\t\t\t '
DATA_TAB_4 = '\t\t\t\t '

app = Flask(__name__)

#global variable to store table data
dataArray = []


#unpack ethernet frame
def ethernet_frame(data):
	# struct.unpack format : ! == network, 6s == 6bytes/characters, H=proto
	# What is data[:14]? Start from 0 to the 14th character
	dest_mac, src_mac, proto = struct.unpack('! 6s 6s H', data[:14])
	
	#since the format of the dest_mac and src_mac are not in human readable format, use function get_mac_addr to convert 
	return get_mac_addr(dest_mac), get_mac_addr(src_mac), socket.htons(proto), data[14:]
	
#return properly formatted MAC Address(AA:BB:CC:DD:EE:FF)
def get_mac_addr(bytes_addr):
	bytes_str = map('{:02x}'.format, bytes_addr)
	
	return ':'.join(bytes_str).upper()
	
	
# Unpack IPv4 packet
def ipv4_packet(data):
	#version and header is the 1st byte
	#extract using bitwise
	version_header_length = data[0]
	version = version_header_length >> 4
	header_length = (version_header_length & 15) * 4
	ttl, proto, src, target = struct.unpack('! 8x B B 2x 4s 4s', data[:20])
	return version, header_length, ttl, proto, ipv4(src), ipv4(target), data[header_length:]
	
# returns properly formatted IPv4(e.g 127.0.0.1)
def ipv4(addr):
	return '.'.join(map(str, addr))
	
# Unpack ICMP Packet
def icmp_packet(data):
	icmp_type, code, checksum = struct.unpack('! B B H', data[:4])
	return icmp_type, code, checksum, data[4:]
	
# unpack TCP segment
def tcp_segment(data):
	(src_port, dest_port, sequence, acknowledgement, offset_reserved_flags) = struct.unpack('! H H L L H', data[:14])
	offset = (offset_reserved_flags >> 12) * 4
	flag_urg = (offset_reserved_flags & 32) >> 5
	flag_ack = (offset_reserved_flags & 16) >> 4
	flag_psh = (offset_reserved_flags & 8) >> 3
	flag_rst = (offset_reserved_flags & 4) >> 2
	flag_syn = (offset_reserved_flags & 2) >> 1
	flag_fin = offset_reserved_flags & 1
	return src_port, dest_port, sequence, acknowledgement, flag_urg, flag_ack, flag_psh, flag_rst, flag_syn, flag_fin, data[offset:]
	
# Unpacks UDP segment
def udp_segment(data):
	src_port, dest_port, size = struct.unpack('! H H 2x H', data[:8])
	return src_port, dest_port, size, data[8:]
	
# Formats multi-line data
def format_multi_line(prefix, string, size=80):
	size -= len(prefix)
	if isinstance(string, bytes):
		string = ''.join(r'\x{:02x}'.format(byte) for byte in string)
		if size % 2:
			size -= 1
	return '\n'.join([prefix + line for line in textwrap.wrap(string, size)])
	

# detect malicious packets against config.txt
def detect(protocol, source, src_port, destination, dest_port):
	f = open('config.txt', 'r')
	
	severityLevel = "None"

	for x in f:
		# ignore comments in config file
		if "#" not in x:
		
			data=x.split(' ')
			config_proto = data[0]
			config_source_addr = data[1]
			config_src_port = data[2]
			config_dest_addr = data[4]
			config_dest_port = data[5]
			severity = data[6]
		

			if(config_src_port != "any") or (config_dest_port != "any"):
				if(protocol == config_proto) and (source == config_source_addr) and (src_port == config_src_port) and (destination == config_dest_addr) and (dest_port == config_dest_port):
					severityLevel = severity
			else:
				if(protocol == config_proto) and (source == config_source_addr) and (destination == config_dest_addr):
					severityLevel = severity 
	
	return severityLevel	
	

@app.route("/")
def main():
	conn = socket.socket(socket.PF_PACKET, socket.SOCK_RAW, socket.ntohs(3))
	
	
	while True:
		# Capture data in network
		raw_data, addr = conn.recvfrom(65536)
		
		#format data
		dest_mac, src_mac, eth_proto, data = ethernet_frame(raw_data)
		
		# Do not print localhost data
		if dest_mac != "00:00:00:00:00:00" and src_mac != "00:00:00:00:00:00":
			# 8 for ipv4
			if eth_proto == 8:
				(version, header_length, ttl, proto, src, target, data) = ipv4_packet(data)
				
		
				print(TAB_1 + 'IPv4 Pakcet: ')
				print(TAB_2 + 'Version: {}, Header Length: {}, TTL: {}'.format(version, header_length, ttl))
				print(TAB_2 + 'Protocol: {}, Source: {}, Target: {}'.format(proto, src, target))
				
				headings = ["Source IP", "Source Port", "Destination IP", "Destination Port" ,"Protocol", "Severity"]
				
				
				#rowData = [src, target, protocol]
				
				#dataArray.append(rowData)
				
				
				# ICMP
				if proto == 1:
					icmp_type, code, checksum, data = icmp_packet(data)
					
					proto = 'icmp'
					
				
					print(TAB_1 + 'ICMP Packet: ')
					print(TAB_2 + 'Type: {}, Code: {}, Checksum: {}'.format(icmp_type, code, checksum))
					print(TAB_2 + 'Data:')
					print(format_multi_line(DATA_TAB_3, data))
					
					
					severity = detect(proto, src, src_port, target, dest_port)
					rowData = [src, src_port, target, dest_port, proto, severity]
					dataArray.append(rowData)
					
					return render_template("index.html", dataArray=dataArray, headings=headings) 	
				
				# TCP
				elif proto == 6:
					(src_port, dest_port, sequence, acknowledgement, flag_urg, flag_ack, flag_psh, flag_rst, flag_syn, flag_fin, data) = tcp_segment(data)
					
					proto = 'tcp'
					
					print(TAB_1 + 'TCP Segment:')
					print(TAB_2 + 'Source Port: {}, Destination Port: {}'.format(src_port, dest_port))
					print(TAB_2 + 'Sequence: {}, Acknowledgement: {}'.format(sequence, acknowledgement))
					print(TAB_2 + 'Flags:')
					print(TAB_3 + 'URG: {}, ACK: {}, PSH: {}, RST: {}, SYN: {}, FIN: {}'.format(flag_urg, flag_ack, flag_psh, flag_rst, flag_syn, flag_fin))
					print(TAB_2 + 'Data:')
					print(format_multi_line(DATA_TAB_3, data))
					# *****data*****??
					
					
					severity = detect(proto, src, src_port, target, dest_port)
					rowData = [src, src_port, target, dest_port, proto, severity]
					dataArray.append(rowData)
					
					#TESTING - GET INFO TABLE ID
					infoTable = document.getElementById("info_table").id
					print("#TESTING - GET INFO TABLE ID: ", infoTable)
					
					
					return render_template("index.html", dataArray=dataArray, headings=headings) 
					
				#UDP
				elif proto == 17:
					src_port, dest_port, length, data = udp_segment(data)
					
					proto = 'udp'
					
					print(TAB_1 + 'UDP Segment:')
					print(TAB_2 + 'Source Port: {}, Destination Port: {}, Length: {}'.format(src_port, dest_port, length))
					
					severity = detect(proto, src, src_port, target, dest_port)
					rowData = [src, src_port, target, dest_port, proto, severity]
					dataArray.append(rowData)
					
					return render_template("index.html", dataArray=dataArray, headings=headings) 
			else:
				
				print('Data:')
				print(format_multi_line(DATA_TAB_1, data))


if __name__ == '__main__':
	main()
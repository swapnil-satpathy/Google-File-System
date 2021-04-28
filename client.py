import socket
import os
import sys
import math
import config
import threading
from socket import AF_INET, SOCK_STREAM
import utility



def sendtoParticularChunkserver(fp,client_to_chunkserver_socket,chunk_no,offset):
	chunk_number=utility.integerToString(chunk_no)
	client_to_chunkserver_socket.send(str.encode(chunk_number))
	actualId=chunk_no-offset
	fp.seek((actualId-1)*config.CHUNK_SIZE)
	chunk_data=fp.read(config.CHUNK_SIZE)
	length_of_chunk_data=len(chunk_data)
	temp=utility.integerToString(length_of_chunk_data)
	client_to_chunkserver_socket.send(str.encode(temp))
	counter = 0

	while length_of_chunk_data:
		data=chunk_data[counter:counter+config.MESSAGE_SIZE]
		client_to_chunkserver_socket.send(data)
		length_of_chunk_data-=len(data)
		counter+=len(data)

	print(f"{chunk_no} sent")




def sendChunksToChunkServers(ip,port,chunk_numbers,file_name,offset):
	client_to_chunkserver_socket=socket.socket(AF_INET, SOCK_STREAM)
	try:
		client_to_chunkserver_socket.connect((ip, port))
	except:
		print(f"Cannot connect to the chunkserver with ip: {ip} and port: {port}")

	# This is done to identify in the chunkserver side that the message is from client
	f_name = f"C|{file_name}|"
	f_name = f_name + '\0'*(config.MESSAGE_SIZE - len(f_name))

	print("The file name sent is ",f_name)
	client_to_chunkserver_socket.send(str.encode(f_name))

	num_chunks = utility.integerToString(len(chunk_numbers))

	client_to_chunkserver_socket.send(str.encode(num_chunks))


	fp=open(file_name, "rb")
	for chunk_no in chunk_numbers:
		temp=sendtoParticularChunkserver(fp,client_to_chunkserver_socket,chunk_no,offset)
		# if temp == -1:
		# 	break

	fp.close()
	client_to_chunkserver_socket.close()


def uploadFile(file_name):
	if not os.path.isfile(file_name):
		print(f"The file you provided, {file_name}, is not found.")
		return
	s=socket.socket()
	master_server_ip=config.master_server_ip
	master_server_port=config.master_server_port
	try:
		s.connect((master_server_ip,master_server_port))
		print("Connected with Master Server for uploading a file")
	except ConnectionRefusedError :
		print("Failed to connect to Master Server")
	file_size=os.path.getsize(os.getcwd()+"/"+file_name)
	file_hash=utility.calculateHash(file_name)
	#This is the format in which the string will be send from client
	str_to_send = "|".join(["U", file_name, str(file_size), file_hash, ""])
	# We are padding the message to a size of 1024 is the message size is less than 1kB
	str_to_send = str_to_send + (config.MESSAGE_SIZE - len(str_to_send))*'\0'

	#encode the string into bytes
	str_to_send_in_bytes=str.encode(str_to_send)
	print(f"Sending {len(str_to_send_in_bytes)} of data")
	s.send(str_to_send_in_bytes)

	message_from_server=s.recv(config.MESSAGE_SIZE).decode()
	print(f"This is the message from server: {message_from_server}")
	print("\n")

	'''
	Message from server format: M|1,5:127.0.0.1:3333|2:127.0.0.1:4444|3,4:127.0.0.1:5555|
	Message after Formatting : [['1,5', '127.0.0.1', 3333], ['2', '127.0.0.1', 4444]]
	'''

	data=message_from_server.split('|')
	data=data[1:len(data)]
	# print("The length of a is :", len(a))
	# data = data[:-1]
	data=data[:-1]
	# print("This is the data")
	# print(a)
	message_from_server_after_parsing=[]
	for i in data:
		message_from_server_after_parsing.append(i.split(":"))
	for j in message_from_server_after_parsing:
		j[2] = int(j[2])


	print("Message after Formatting: ",message_from_server_after_parsing)
	print("\n")

	threads=[]
	offset=None

	for chunks,ip,port in message_from_server_after_parsing:
		chunk_numbers=list(map(int,chunks.split(",")))
		if offset is None:
			offset=chunk_numbers[0]-1
		thread=threading.Thread(target=sendChunksToChunkServers,args=[ip, port,chunk_numbers,file_name,offset])
		thread.start()
		threads.append(thread)

	for thread in threads:
		thread.join()

	# msg="A|{}|".format(file_name)
	# msg=msg+"\0"*(config.MESSAGE_SIZE-len(msg))
	# s.send(str.encode(msg))
	s.close()


def downloadFile(file_name):
	download_socket=socket.socket()

	try:
		download_socket.connect((config.master_server_ip,config.master_server_port))
		print ("Connected with master server for Downloading a file")
	except ConnectionRefusedError:
		print("try connecting to BackUp")

	str_to_send="|".join(["D",file_name,""])
	str_to_send = str_to_send + (config.MESSAGE_SIZE - len(str_to_send))*'\0'
	str_to_send_in_bytes=str.encode(str_to_send)
	download_socket.send(str_to_send_in_bytes)

	# Handling the message received from master server
	file_names=download_socket.recv(config.MESSAGE_SIZE).decode()
	file_names=utility.fileParser(file_names,download_socket)

	if file_names == -1:
		return
	for file_name in file_names:
		message_from_server=download_socket.recv(config.MESSAGE_SIZE).decode()
		print("This below is the reply from master server in download")
		print(message_from_server)

		if message_from_server[0] == 'S':
			print(f'{file_name} is currently not available will try again after 20 seconds')
			message_from_server=download_socket.recv(config.MESSAGE_SIZE).decode()
		elif message_from_server[0] == 'F':
			print('f{file_name} is blocked')

		else:
			message_from_server2=download_socket.recv(config.MESSAGE_SIZE).decode()
			message_from_server2_splitted=message_from_server2.split("|")
			file_hash_value=""
			if message_from_server2_splitted[0] == 'Z':
				file_hash_value=message_from_server2_splitted[1]

	download_socket.close()
	#This commented below logic to be seen after
	# if len(file_names) == 1:
	# 	return
	# output_name=file_names[0]
	# for file_name in file_names[:-1]:
	# 	os.remove(file_name)
	# os.remove(file_names[-1],output_name)















def upload(file_names):
	for file_name in file_names:
		uploadFile(file_name)

def download(file_names):
	for file_name in file_names:
		downloadFile(file_name)

def lease(file_name):
	lease_socket=socket.socket()
	try:
		lease_socket.connect((config.master_server_ip,config.master_server_port))
		print ("Connected with master server for putting lease on a file")
	except ConnectionRefusedError:
		print("try connecting to BackUp")
	str_to_send="|".join(["L",file_name[0],""])
	str_to_send = str_to_send + (config.MESSAGE_SIZE - len(str_to_send))*'\0'
	lease_socket.send(str.encode(str_to_send))




def update(args):
	old_file,new_file = args[0],args[1]
	str_to_send=f"Up|{old_file}|{new_file}|"
	str_to_send = str_to_send + (config.MESSAGE_SIZE - len(str_to_send))*'\0'
	update_socket=socket.socket()
	try:
		update_socket.connect((config.master_server_ip,config.master_server_port))
		print ("Connected with master server for updating a file")
	except ConnectionRefusedError:
		print("try connecting to BackUp")

	update_socket.send(str.encode(str_to_send))
	update_socket.close()
	uploadFile(new_file)







if __name__ == '__main__':
	while True:
		args = input()
		# print(args)
		args_split=args.split()
		command=args_split[0]

		if (command == "exit"):
			sys.exit()
		 # the upload syntax is upload file1 file2 file3...
		elif (command == "upload"):
			upload(args_split[1:])
		elif (command == "download"):
			download(args_split[1:])
		elif (command == "lease"):
			lease(args_split[1:])

		# The update syntax is update old_file new_file
		elif (command == "update"):
			update(args_split[1:])

		else:
			print("Please give a valid action to perform")
			sys.exit()

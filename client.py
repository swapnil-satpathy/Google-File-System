import socket
import os
import pickle
import sys
import math
import hashlib
import config

def calculateHash(file_name):
	sha1_value=hashlib.sha1()
	with open(file_name,'rb') as fp:
		while True:
			data = fp.read(65536) #65536 is the buffer size for hash calculation
			if not data:
				break
			sha1_value.update(data)

	return sha1_value.hexdigest()



def uploadFile(file_name):
	if not os.path.isfile(file_name):
		print(f"The file you provided, {file_name}, is not found.")
		return
	s=socket.socket()
	master_server_ip=config.master_server_ip
	master_server_port=config.master_server_port
	s.connect((master_server_ip,master_server_port))
	file_size=os.path.getsize(os.getcwd()+"/"+file_name)
	file_hash=calculateHash(file_name)
	#This is the format in which the string will be send from client
	str_to_send = "|".join(["U", file_name, str(file_size), file_hash, ""])
	# We are padding the message to a size of 1024 is the message size is less than 1kB
	str_to_send = str_to_send + '\0'*(config.MESSAGE_SIZE - len(str_to_send))

	#encode the string into bytes
	str_to_send_in_bytes=str.encode(str_to_send)
	print(f"Sending {len(str_to_send_in_bytes)} of data")
	s.send(str_to_send_in_bytes)

	message_from_server=s.recv(config.MESSAGE_SIZE).decode()
	print(f"This is the message from server: {message_from_server}")







def upload(file_names):
	for file_name in file_names:
		uploadFile(file_name)






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
		elif (command == "update"):
			update(args_split[1:])

		else:
			print("Please give a valid action to perform")
			sys.exit()

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

def stringToInteger(message):
    message_splitted=message.split("|")

    # DENOTES NUMBER
    if message_splitted[0] == "N":
        return int(message_splitted[1])
    return None


def integerToString(message_splitted):
    message=f"N|{message_splitted}|"
    message+='\0'*(config.MESSAGE_SIZE-len(message))
    return message


def fileParser(file_names,download_socket):
    file_names_splitted=file_names.split("|")
    if file_names_splitted[0] == 'f':
        file_name=[x.strip() for x in file_names_splitted[1:-1]]
        return file_name
    return_value=None
    if file_names_splitted[0] == 'S':
        print(f'File currently not availble, will try again in 20 seconds')
        return_value=download_socket.recv(config.MESSAGE_SIZE).decode()

    if file_names_splitted[0] == 'F':
        print(f'The file is blocked')
        return -1
    vals=return_value.split("|")
    return [x.strip() for x in vals[1:-1]]

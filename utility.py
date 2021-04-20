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
    return_value=None
    if file_names_splitted[0] == 'f':
        file_name=[]
        for x in vals[1:-1]:
            file_name.append(x.strip())
        return file_name
    if file_names_splitted[0] == 'F':
        print(f'File is blocked')
        return -1

    if file_names_splitted[0] == 'S':
        print(f'File currently not available,will abort in 20 seconds if not available ...')
        return_value=download_socket.recv(config.MESSAGE_SIZE).decode()
    return_value_splitted=return_value.split("|")
    if return_value_splitted[0]!='f':
        return -1
    return [file_name.strip() for file_name in return_value_splitted[1:-1]]

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

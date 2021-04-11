import config
import math


#The below function returns the number of chunks that the file will be divided in
def numberOfChunks(file_size):
    return math.ceil(file_size/config.CHUNK_SIZE)


def upload(message_from_client_split):
    file_name=message_from_client_split[1]
    file_size=int(message_from_client_split[2])
    file_hash=message_from_client_split[3]
    no_of_chunkservers=config.NO_OF_CHUNKSERVERS
    no_of_chunks=numberOfChunks(file_size)
    print(f"{file_name} has {no_of_chunks} number of chunks")

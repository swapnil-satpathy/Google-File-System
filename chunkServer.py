import socket
import os
import sys
import math
import config
import threading
import utility


'''
In the command line arguments you will have to provide the chunkserver number.
So for ex: if this is the 3rd chunkserver then in the command line argument you
will have to provide 3
'''

argc=len(sys.argv)
if(argc<2):
    print("Please provide the chunkserver number")
    sys.exit()
chunkserver_number=int(sys.argv[1])
chunkserver_ip=config.chunk_servers_ip[chunkserver_number-1]
chunkserver_port=config.chunk_servers_port[chunkserver_number-1]
chunkServerSocket=socket.socket()
chunkServerSocket.bind((chunkserver_ip,chunkserver_port))
chunkServerSocket.listen(5)

def receiveFile(client_socket,file_name):
    number_of_chunks = client_socket.recv(config.MESSAGE_SIZE).decode()
    number_of_chunks=utility.stringToInteger(number_of_chunks)

    print("Number of Chunks", number_of_chunks)
    print("\n")
    for i in range(0,number_of_chunks):
        chunk_no=client_socket.recv(config.MESSAGE_SIZE).decode()
        chunk_no=utility.stringToInteger(chunk_no)
        print("The below is printed in the Chunkserver")
        print("The chunk Number = ", chunk_no)
        print("\n")
        fp=open(f"{chunk_no}.chunk","wb")
        length_of_chunk_data=client_socket.recv(config.MESSAGE_SIZE).decode()
        length_of_chunk_data=utility.stringToInteger(length_of_chunk_data)
        while length_of_chunk_data:
            data=client_socket.recv(config.MESSAGE_SIZE)
            fp.write(data)
            length_of_chunk_data-=len(data)
        fp.close()
        print(f"Chunk {chunk_no} written in chunkserver")
    client_socket.close()



def listening(client_socket,client_addr):
    message=client_socket.recv(config.MESSAGE_SIZE).decode()
    message_split=message.split("|")
    if message_split[0] == "C":
        receiveFile(client_socket,message_split[1])
    elif message_split[0]=="H":
        pass
    elif message_split[0]=="R":
        pass
    elif message_split[0]=="X":
        pass
    elif message_split[0]=="t":
        pass


while True:
    client_socket,client_addr=chunkServerSocket.accept()
    thread=threading.Thread(target=listening,args=[client_socket,client_addr])
    thread.start()
chunkServerSocket.close()

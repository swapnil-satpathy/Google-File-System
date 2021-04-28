import socket
import os
import pickle
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

def replicateChunks(message):
    chunks,ip,port=message.split(':')
    chunks = list(map(int, chunks.split(",")))
    port = int(port)
    chunkserver_socket=socket.socket()
    chunkserver_socket.connect((ip,port))
    message = "t|{}|".format(len(chunks))
    message = message+'\0'*(config.MESSAGE_SIZE-len(message))
    chunkserver_socket.send(str.encode(message))

    for chunk_no in chunks:
        message=utility.integerToString(chunk_no)
        chunkserver_socket.send(str.encode(message))
        with open("chunk/{}.chunk".format(chunk_no), "wb") as fp:
            msg = chunkserver_socket.recv(config.MESSAGE_SIZE).decode()
            file_size = utility.stringToInteger(msg)
            temp=file_size
            data=0
            while temp>0:
                d=chunkserver_socket.recv(config.MESSAGE_SIZE)
                data+=len(d)
                fp.write(d)
                temp-=len(d)

            print("Total Data Recieved ",data)
            print("REPLICATED CHUNK {}".format(chunk_no))

    chunkserver_socket.close()











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
     fp=open(f"chunks/{chunk_no}.chunk","wb")
     length_of_chunk_data=client_socket.recv(config.MESSAGE_SIZE).decode()
     length_of_chunk_data=utility.stringToInteger(length_of_chunk_data)
     while length_of_chunk_data:
         data=client_socket.recv(config.MESSAGE_SIZE)
         fp.write(data)
         length_of_chunk_data-=len(data)
     fp.close()
     print(f"Chunk {chunk_no} written in chunkserver")
 client_socket.close()

def sendReplicationChunks(client_socket,no_of_chunks):
    no_of_chunks=int(no_of_chunks)
    for i in range(no_of_chunks):
         message=client_socket.recv(config.MESSAGE_SIZE)
         chunk_no=utility.stringToInteger(message)
         with open("chunk/{}.chunk".format(chunk_no), "rb") as fp:
             file_size =os.path.getsize("chunk/{}.chunk".format(chunk_no))
             message=utility.integerToString(file_size)
             client_socket.send(str.encode(message))
             temp = file_size
             data=fp.read()
             count = 0
             while temp>0:
                 d = data[count:count+MESSAGE_SIZE]
                 count+=len(d)
                 client_socket.send(d)
                 temp-=len(d)
            



# As there are many messages being sent to the chunkserver for client
# and masterserver and also various kind of messages, we are differentiating
# between different kind of messages by the keywords which are added before
# the actual messages. It helps in differentiating the kind of operation needed
# as we can see below

def listening(client_socket,client_addr):
 message=client_socket.recv(config.MESSAGE_SIZE).decode()
 message_split=message.split("|")
 if message_split[0] == "C":
     receiveFile(client_socket,message_split[1])
 elif message_split[0]=="R":
     replicateChunks(message_split[1])
 elif message_split[0]=="X":
     pass
 elif message_split[0]=="t":
     sendReplicationChunks(client_socket,message_split[1])


while True:
 client_socket,client_addr=chunkServerSocket.accept()
 thread=threading.Thread(target=listening,args=[client_socket,client_addr])
 thread.start()
chunkServerSocket.close()

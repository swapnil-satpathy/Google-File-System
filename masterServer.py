import socket
import threading
import os
import math
import sys
import json
import copy
import config
from upload import upload
import dS
import time
from lease import lease
from update import update
from download import download


# def makeBackUp():


def backupServer():
    while True:
        pass
        # makeBackUp()
        # time.sleep(10)






def checkIfActive(chunk_index):
    chunkserver_IP=config.chunk_servers_ip[chunk_index]
    chunkserver_port=int(config.chunk_servers_port[chunk_index])
    flag = 0
    chunkserver_socket=socket.socket()
    chunkserver_socket.settimeout(1)

    # Here we are trying to connect to the chunkserver and
    # if we are getting connectionrefused error then we are
    # concluding that the Chunkserver is down. An addition check
    # that can be done is to send some dummy message to the particular
    # message and wait for it to reply with some acknowledgment

    try:
        chunkserver_socket.connect((chunkserver_IP,chunkserver_port))
    except ConnectionRefusedError:
        flag=1

    ip_port=chunkserver_IP+":"+str(chunkserver_port)
    # If a chunkserver is down
    if flag == 1:
        print(f"The chunkserver {chunk_index+1} is down")
        if dS.dict_status_bit[ip_port] == 'A':
            dS.dict_status_bit[ip_port]='C'
            handleChunkServerDown(ip_port)
        elif dS.dict_status_bit[ip_port] == 'C':
            dS.dict_status_bit[ip_port]='D'
    # If the chunkserver is not down
    elif flag == 0:
        dS.dict_status_bit[ip_port]='A'
    chunkserver_socket.close()







def createStatus():
    for i in range(0,len(config.chunk_servers_ip)):
        dS.dict_status_bit[config.chunk_servers_ip[i]+":"+str(config.chunk_servers_port)]


def heartBeat():
    while True:
        for i in range(0,len(config.chunk_servers_ip)):
            checkIfActive(i)
        print(dS.dict_status_bit)
        time.sleep(10)


# Accept requests from client/chunkserver and process accordingly
def listening(message_from_client,client_socket):
    message_from_client_split=message_from_client.split("|")
    command=message_from_client_split[0]
    print("The command from client is",command)
    # If the client wants to upload
    if (command == 'U'):
        str_to_return=upload(message_from_client_split)
        str_to_return_in_bytes=str.encode(str_to_return)
        client_socket.send(str_to_return_in_bytes)
        client_socket.close()



    #If the client wants to download
    elif(command == 'D'):
        return_value_from_download=download(message_from_client,client_socket)
        print("This below is the return value from download.py")
        print(return_value_from_download)
        if return_value_from_download[0] == 'S':
            str_to_return_in_bytes=str.encode(return_value_from_download)
            client_socket.send(str_to_return_in_bytes)
            time.sleep(20)
            return_value_from_download=download(message_from_client,client_socket,'S')
        if return_value_from_download[0] == 'F':
            str_to_return_in_bytes=str.encode(return_value_from_download)
            client_socket.send(str_to_return_in_bytes)
            client_socket.close()







    #If the client wants to put lease on the file
    elif(command == 'L'):
        lease(message_from_client)
    #if the client wants to update any file
    elif(command == 'Up'):
        old_file=message_from_client[1]
        new_file=message_from_client[2]
        update(old_file,new_file)






def masterListen():
    # Create a socket object
    s=socket.socket()
    s.bind((config.master_server_ip,config.master_server_port))
    s.listen(5)
    while True:
        client_socket,client_addr=s.accept()
        message_from_client=client_socket.recv(config.MESSAGE_SIZE).decode()
        print(message_from_client)
        print("\n")
        thread1=threading.Thread(target=listening,args=(message_from_client,client_socket,))
        thread1.start()
    s.close()




if __name__ == '__main__':
    createStatus()
    thread1=threading.Thread(target = heartBeat)
    thread1.start()
    thread2=threading.Thread(target=backupServer)
    thread2.start()
    masterListen()

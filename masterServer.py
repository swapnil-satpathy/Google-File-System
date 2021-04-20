import socket
import threading
import os
import math
import pickle
import sys
import json
import copy
import config
from upload import upload
import dS
import time
from download import download
from lease import lease








# Accept requests from client/chunkserver and process accordingly
def listening(message_from_client,client_socket):
    message_from_client_split=message_from_client.split("//")
    command=message_from_client_split[0]
    # If the client wants to upload
    if (command == 'U'):
        str_to_return=upload(message_from_client_split)
        str_to_return_in_bytes=str.encode(str_to_return)
        client_socket.send(str_to_return_in_bytes)
        client_socket.close()



    #If the client wants to download
    elif(command == 'D'):
        str_to_return=download(message_from_client,client_socket)
        if str_to_return[0] == 'S':
            str_to_return_in_bytes=str.encode(str_to_return)
            client_socket.send(str_to_return_in_bytes)
            time.sleep(20)
            str_to_return=download(message_from_client,client_socket,'S')
        if str_to_return[0] == 'F':
            str_to_return_in_bytes=str.encode(str_to_return)
            client_socket.send(str_to_return_in_bytes)
            client_socket.close()





    #If the client wants to put lease on the file
    elif(command == 'L'):
        lease(message_from_client)
    #if the client wants to update any file
    elif(command == 'Up'):
        pass






def master_listen():
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
    #  heartbeat code
    while True:
        master_listen()

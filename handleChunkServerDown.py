import dS
import config
import socket




def findChunkServers(ip_port):
    chunk_server_list=[]
    first=''
    second=''
    third=''
    for key in dS.dict_status_bit.keys():
        chunk_server_list.append(key)
    i = len(chunk_server_list)-1
    while(chunk_server_list[i]!=ip_port):
        i = (i-1) %len(chunk_server_list)
    while(dS.dict_status_bit[chunk_server_list[i]] != 'A'):
        i = (i-1) %len(chunk_server_list)
    first = chunk_server_list[i]
    i=0
    while(chunk_server_list[i] != ip_port):
        i = (i+1) %len(chunk_server_list)
    while(dS.dict_status_bit[chunk_server_list[i]] != 'A'):
        i = (i+1) %len(chunk_server_list)
    second = chunk_server_list[i]
    i = (i+1) %len(chunk_server_list)
    while(dS.dict_status_bit[chunk_server_list[i]] != 'A'):
        i = (i+1) %len(chunk_server_list)
    third = chunk_server_list[i]
    return [first,second,third]


def connect_when_replica(ip_port,str_to_send):
    chunk_server_ip=ip_port.split(':')[0]
    chunk_server_port=int(ip_port.split(':')[1])
    chunkserver_socket=socket.socket()
    chunkserver_socket.connect((chunk_ip,chunk_port))
    message=str_to_send+(config.MESSAGE_SIZE - len(str_to_send))*'\0'
    chunkserver_socket.send(str.encode(message))
    chunkserver_socket.close()



def handleChunkServerDown(ip_port):
    primary_list=[]
    secondary_list=[]
    ip_ports=findChunkServers(ip_port)
    for i in ip_ports:
        print(i)
    key=ip_ports[1]
    third=ip_ports[2]
    for file_name in dS.dict_chunk_details:
        primary_list=primary_list+dS.dict_chunk_details[file_name]['P'][ip_port]
        dS.dict_chunk_details[f_name]['P'][key].extend(dS.dict_chunk_details[file_name]['S'][key])
        secondary_list = secondary_list + dS.dict_chunk_details[file_name]['S'][ip_port]
        dS.dict_chunk_details[file_name]['S'][key].clear()
        dS.dict_chunk_details[file_name]['S'][key].extend(dS.dict_chunk_details[file_name]['S'][ip_port])
        dS.dict_chunk_details[file_name]['S'][third].extend(dS.dict_chunk_details[file_name]['P'][ip_port])

    primary_str = 'R|' + ','.join(primary_list) + ':'+ ip_ports[1] + '|'
    secondary_str = 'R|' + ','.join(secondary_list) + ':'+ ip_ports[0] + '|'
    connect_when_replica(ip_ports[2],primary_str)
    connect_when_replica(ip_ports[1],secondary_str)

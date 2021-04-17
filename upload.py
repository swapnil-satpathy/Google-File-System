import config
import math
import dS



#The below function returns the number of chunks that the file will be divided in
def numberOfChunks(file_size):
    return math.ceil(file_size/config.CHUNK_SIZE)

def createDictChunkServer(ip_port_info,chunkId_chunkserver_mapping):
    counter=0
    for ip_port in ip_port_info:
        temp=[]
        # If already the dict_chunkserver_ids contain the chunk numbers
        # for a specific ip_port, then append them first.. This is done so
        # that we dont have to do deep copies of data Structures and it will
        # lead to less confusion

        if ip_port in dS.dict_chunkserver_ids:
            for ids in dS.dict_chunkserver_ids[ip_port]:
                temp.append(ids)
        for chunks in chunkId_chunkserver_mapping[counter]:
            temp.append(chunks)
        dS.dict_chunkserver_ids[ip_port]=temp
        counter+=1

    # This data structure dict_chunkserver_ids contain the key as
    # ip and port combined of the chunkServers and all the chunks that
    # particular chunkserver contains


    print("This below is the status of the dict_chunkserver_ids")
    print(dS.dict_chunkserver_ids)
    print("\n")






def upload(message_from_client_split):
    file_name=message_from_client_split[1]
    file_size=int(message_from_client_split[2])
    file_hash=message_from_client_split[3]
    no_of_chunkservers=config.NO_OF_CHUNKSERVERS
    no_of_chunks=numberOfChunks(file_size)
    print(f"{file_name} has {no_of_chunks} number of chunks")

    ip_port_info=[]
    for i in range(0,len(config.chunk_servers_ip)):
        temp=str(config.chunk_servers_ip[i])+":"+str(config.chunk_servers_port[i])
        ip_port_info.append(temp)

    '''
    The logic written below calculates which chunk will go to which chunkServerSocket
    chunkId_chunkserver_mapping contains a list of chunks
    For ex: if the state of chunkId_chunkserver_mapping is [[2,3],[4,5],[],[]],
    the above means chunk number 2 and 3 will go to chunkserver 1,
    chunkserver 4 and 5 will go to chunkserver 2 and so on..
    This is done to ensure that the chunks are well distributed within chunkServers
    and there is no traffic in one particular chunkserver
    '''

    chunkId_chunkserver_mapping=list()
    for i in range(1,no_of_chunkservers+1):
        temp = list()
        counter = 0
        while (i+counter*no_of_chunkservers)<=no_of_chunks:
            temp.append(str(i+dS.chunk_id+(counter*no_of_chunkservers)))
            counter+=1
            # print(temp)
        chunkId_chunkserver_mapping.append(temp)

    print("Below is the status of the chunkId_chunkserver_mapping")
    print(chunkId_chunkserver_mapping)
    print("\n")

    dS.chunk_id+=no_of_chunks

    # This dictionary will contain all the file_names being uploaded
    dS.dict_filename_update[file_name]=file_name

    # This dictionary stores the status of the file for lease feature
    dS.dict_file_status[file_name]="A"
    # This dictionary stores the hash value of the file
    dS.dict_file_hash[file_name]=file_hash

    createDictChunkServer(ip_port_info,chunkId_chunkserver_mapping)


    str_to_return=""

    # M - Master to client response.It sends details of all the chunkservers
    #       Format ==> E|chunk_num1,chunk_num2:chunkserver_ip1:chunkserver_port1|
    #                    chunk_num1:chunkserver_ip2:chunkserver_port2
    #       Ex : E|1,5:127.0.0.1:3333|2:127.0.0.1:4444|3,4:127.0.0.1:5555
    str3='M'
    for i in range(0,len(chunkId_chunkserver_mapping)):
        if i == no_of_chunks:
            break
        str1=','.join(chunkId_chunkserver_mapping[i])
        ip_port_split=ip_port_info[i].split(":")
        str2=':'.join([str1,ip_port_split[0],ip_port_split[1]])
        str3='|'.join([str3,str2])
    str3=f"{str3}|"
    str_to_return=str3+(config.MESSAGE_SIZE - len(str3))*'\0'
    print("This is the string returned to the client by master",str_to_return)
    return str_to_return

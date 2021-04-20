import dS
import config
def download(message_from_client,client_socket,state='X'):
    file_name=message_from_client[1]
    if dS.dict_file_status[file_name] == 'A':
        print(dS.dict_chunk_details[file_name]['P'])
        print("dict_chunk_details inside download :",dS.dict_chunk_details)
        print("dict_status_bit inside download :",dS.dict_status_bit)

        temp="f|"
        for filenames in ds.dict_filename_update[file_name]:
            temp+=filenames+"|"
        str_to_return=temp+'\0'*(config.MESSAGE_SIZE-len(temp))
        client_socket.send(str.encode(str_to_return))
        final_string=""
        for file in dS.dict_filename_update[file_name]:
            for key,value in dS.dict_chunk_details[file]['P'].items():
                if dS.dict_status_bit[key]!='A':
                    continue
                chunk_nums=','.join(value)
                temp2 = ':'.join([chunk_nums,key])
                final_string+=temp2+'|'
            str_to_return='E|'+final_string+(config.MESSAGE_SIZE-len(temp))*'\0'
            print("This is the second string from download : ",str_to_return)
            client_socket.send(str.encode(str_to_return))

            str_to_return='Z|'+dS.dict_file_hash[message_from_client[1]]+'|'
            client_socket.send(str.encode(str_to_return))
        client_socket.close()
    else:
        if state == 'S':
            final_string = 'F|101|'
            str_to_return=final_string+(config.MESSAGE_SIZE-len(temp))*'\0'
            return str_to_return
        else:
            final_string = 'S|101|'
            str_to_return=final_string+(config.MESSAGE_SIZE-len(temp))*'\0'
            return str_to_return

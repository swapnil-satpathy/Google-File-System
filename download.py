import dS
import config

def download(message_from_client,client_socket,state='X'):
    print("Entering the download.py file")
    file_name=message_from_client.split('|')[1]
    if dS.dict_file_status[file_name] == 'A':
        final_str=""

        str_name="f|"
        for file in dS.dict_filename_update[file_name]:
            str_name+=file+"|"
        str_to_return=str_name+(config.MESSAGE_SIZE - len(str_name))*'\0'
        client_socket.send(str.encode(str_to_return))

        for file in dS.dict_filename_update[file_name]:
            for key,value in dS.dict_chunk_details[file]['P'].items():
                if dS.dict_status_bit[key]!='A':
                    continue
                chunk_numbers=','.join(value)
                temp_str=':'.join([chunk_numbers,key])
                final_str+=temp_str+'|'

            final_str='E|'+final_str
            str_to_return=final_str+(config.MESSAGE_SIZE - len(final_str))*'\0'
            str_to_return_in_bytes=str.encode(str_to_return)
            client_socket.send(str_to_return_in_bytes)

            str_to_return='Z|'+dS.dict_file_hash[message_from_client.split('|')[1]]+'|'
            str_to_return=str_to_return+(config.MESSAGE_SIZE - len(str_to_return))*'\0'
            print("This is printed in download file")
            print(str_to_return)
            str_to_return_in_bytes=str.encode(str_to_return)
            client_socket.send(str_to_return_in_bytes)
        client_socket.close()


    else:
        if state == 'S':
            str_to_return='F|101|'
            str_to_return=str_to_return+(config.MESSAGE_SIZE - len(str_to_return))*'\0'
            return str_to_return

        else:
            str_to_return='S|101|'
            str_to_return=str_to_return+(config.MESSAGE_SIZE - len(str_to_return))*'\0'
            return str_to_return

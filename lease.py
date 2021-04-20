import dS

def lease(message_from_client):
    file_name=message_from_client[1]

    # change status for that file
    dS.dict_file_status[file_name]="B"
    time.sleep(60)
    # For 60 seconds or 1 minute I am blocking the file
    dS.dict_file_status[file_name]="A"

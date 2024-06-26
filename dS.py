'''

This python file contains all the global Data Structures
(Especially all the dictionaries), which helps the master server in
storing the meta-data about the chunks of a particular file and
which chunkserver holds these chunks.

'''




chunk_id=1
dict_chunk_details={}
dict_all_chunk_info={}

# This dictionary contains the file size of the files
dict_size_info={}

# This dictionary contains the status for all the files.
# Status contains whether this particular file is in lease or not
dict_status_bit={}

# This data structure dict_chunkserver_ids contain the key as
# ip and port combined of the chunkServers and all the chunks that
# particular chunkserver contains
dict_chunkserver_ids={}

 #to store the status of file for lease feature
dict_file_status={}

#to store hash value of the files
dict_file_hash={}

#to store mapping of file name as list of multiple files for update feature
dict_filename_update={}

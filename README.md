# Google-File-System
An Implementation of the Google File System : a distributed File System which inspired Hadoop


How to run the code:-

1) python3 masterServer.py

2) python3 chunkServer.py the chunkserver number

 For ex: If you want to run the first chunkserver then python3 chunkServer.py 1
 
3) python3 client.py

   Then for running any functionality
   
   i) upload file1 file2 file3 -> To upload the list of files given by their file names
   
   ii) downlaod file1 file2 file3 -> To download the list of files given by their file names
   
   iii) lease file1  -> To perform lease on a file
   
   iv) update file1 file2 file3 -> To perform update on the list of file names
   
   v) exit -> to stop the master server

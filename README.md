# DFS
Distributed File System Task for Scalable Computing course at Trinity College Dublin
<br/>The Transparent Distributed File System with Locking and Caching is implemented under TDFS folder
<br/>The Directory Server has been implemented inside the folder Directory Server.

<br/># TDFS with Locking and Caching
<br/>The fileserver can be started by running the folowing command with the port:
<br/>python Client.py 8001

<br/><br/>The clients can be started by running following command with the ipaddress and port of the server:
<br/>python fileServer.py ipaddress 8001
  
<br/><br/>This will output a list of options to the user to run various functionalities

<br/>#Directory File Service
<br/>The two file servers fileServer1 and fileServer2 can be run using the following commands:
<br/>python fileServer1.py port
<br/>python fileServer2.py port

<br/>The directory server can be run using the followign command:
<br/>python fileServer1.py IP1 Port1 IP2 Port2 Port3
<br/>IP1: IP address of fileserver 1
<br/>Port1: Port of fileserver1
<br/>IP2: IP address of fileserver 2
<br/>Port2: Port of fileserver 2
<br/>Port3: Port of directory Server

<br/>Similarly, the client server can be started using command:
python Client.py ipaddress port

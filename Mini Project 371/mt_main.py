# Include Python's Socket Library
from socket import *
import time
import os
import threading

# Specify Server Port
serverPort = 8002

# Create TCP welcoming socket
serverSocket = socket(AF_INET,SOCK_STREAM)

# Bind the server port to the socket
serverSocket.bind(('',serverPort))

# Server begins listerning foor incoming TCP connections
serverSocket.listen(5)
print('The server is ready to receive from port %s ...' % serverPort)

#Threaded function that creates multiple connection that run parallel
def ThreadedServer(connectionSocket,addr):
	print("Connection with :" + addr[0] + " " + str(addr[1]) )

	# Read from socket (but not address as in UDP)
	request=""
	request = connectionSocket.recv(1024).decode()

	#print(request.split('\n')[0])
	if(request!=""):
		#print("Connection with :" + addr[0] + " " + str(addr[1]) )
		response = handle_req(request)
		print("Response for connection with:" + addr[0] + " " + str(addr[1]))
		print(response.split('\n')[0])

		# Send the reply
		connectionSocket.sendall(response.encode())

		# Close connectiion too client (but not welcoming socket)
		connectionSocket.close() 

#function to get the filename eg: test.html from request
def get_filename(request,filename):
	
	for elem in request.split():
		if elem[0] == '/':
			filename = elem[1:]
	return  filename

def get_req_type(request):
	req_type = request.split('/')[0]
	return req_type

def get_content(filename):
	f = open(filename)
	file_content = f.read()
	f.close()
	return file_content

def handle_req(request):
	header = request.split('\n')
	#print(header) 
	filename = ""
	req_type = get_req_type(request)
	filename = get_filename(request,filename)

	#print(req_type)
	if filename!= "":
		while True:
			time_start= time.time()
			try:

				#get contents for HTML file
				file_content= get_content(filename)

				#get modified time and created time of the HTML file
				last_modified_time= time.ctime(os.path.getmtime(filename)) 
				created_time = time.ctime(os.path.getctime(filename))
				#print(last_modified_time)
				#print(created_time)

				#Uncomment time.sleep(10) to check CODE 408 REQUEST TIMEOUT
				#time.sleep(10)
				
				#last_access_time = time.ctime(os.path.getatime(filename))
				time_end = time.time()

				#CODE 408 REQUEST TIMED OUT
				if(time_end - time_start > 1):
					return 'HTTP/1.1 408 REQUEST TIMEOUT\n\n 408 REQUEST TIMED OUT'
					break

				#CODE 200 OK
				elif(created_time!=last_modified_time):
					return 'HTTP/1.1 200 OK\n\n' + file_content

				#CODE 304 NOT MODIFIED
				else:
					return 'HTTP/1.1 304 NOT MODIFIED\n\n 304 NOT MODIFIED'
					
				#print(file_content)

			#CODE 404 NOT FOUND
			except FileNotFoundError:
				return 'HTTP/1.1 404 NOT FOUND\n\n 404 NOT FOUND'	

	#CODE 400 BAD REQUEST  
	else:
		return 'HTTP/1.1 400 BAD REQUEST\n\n 400 BAD REQUEST'

    			


	



while True:

	# Server waits on accept for incoming requests.
    # New socket created on return
	connectionSocket, addr = serverSocket.accept()
	
	#Calling the threaded function, using threading
	ServerThread = threading.Thread(target = ThreadedServer, args= [ connectionSocket, addr])
	ServerThread.start()


serverSocket.close()

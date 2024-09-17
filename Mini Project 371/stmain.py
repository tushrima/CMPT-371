# Include Python's Socket Library
from socket import *
import time
import os

# Specify Server Port
serverPort = 8020

# Create TCP welcoming socket
serverSocket = socket(AF_INET,SOCK_STREAM)

# Bind the server port to the socket
serverSocket.bind(('',serverPort))

# Server begins listerning foor incoming TCP connections
serverSocket.listen(1)
print('The server is ready to receive from port %s ...' % serverPort)

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

#main function to handle requests sent as arguement
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
				#print(file_content)

				#get modified time and created time of the HTML file
				last_modified_time= time.ctime(os.path.getmtime(filename)) 
				created_time = time.ctime(os.path.getctime(filename))

				#print(last_modified_time)
				#print(created_time)


                #Need to uncomment to test 408 REQUEST TIMED OUT
				#time.sleep(3)

				
				
				time_end = time.time()

				#CODE 408 REQUEST TIMED OUT
				if(time_end-time_start > 1):
					return 'HTTP/1.1 408 REQUEST TIMEOUT\n\n 408 REQUEST TIMED OUT'
					# break
				
				#CODE 200 OK
				elif(created_time!=last_modified_time):
					return 'HTTP/1.1 200 OK\n\n' + file_content
					# break
				
				#CODE 304 NOT MODIFIED
				else:
					return 'HTTP/1.1 304 NOT MODIFIED\n\n 304 NOT MODIFIED'

					# break
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

	# Read from socket (but not address as in UDP)
	request =''
	request = connectionSocket.recv(1024).decode()
	#connectionSocket.settimeout(2.9)
	if(request!=''):

		print(request.split('\n')[0])
		response= handle_req(request) 
		print(response.split('\n')[0])

		# Send the reply
		a = response.encode()
		connectionSocket.sendall(a)

		# Close connectiion too client (but not welcoming socket)
		connectionSocket.close() 

serverSocket.close()

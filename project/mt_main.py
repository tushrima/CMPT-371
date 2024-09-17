from socket import *
import time
import os
import concurrent.futures

serverPort = 1113
serverSocket = socket(AF_INET,SOCK_STREAM)
serverSocket.bind(('',serverPort))
serverSocket.listen(5)
print('The server is ready to receive from port %s ...' % serverPort)
global request_type
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
				file_content= get_content(filename)
				last_modified_time= time.ctime(os.path.getmtime(filename)) 
				created_time = time.ctime(os.path.getctime(filename))
				#print(last_modified_time)
				#print(created_time)
				#time.sleep(10)
				time_end = time.time()
				#last_access_time = time.ctime(os.path.getatime(filename))
				time_end = time.time()
				if(time_end - time_start > 1):
					return 'HTTP/1.1 408 REQUEST TIMEOUT\n\n 408 REQUEST TIMED OUT'
					break
				elif(created_time!=last_modified_time):
					return 'HTTP/1.1 200 OK\n\n' + file_content
				else:
					return 'HTTP/1.1 304 NOT MODIFIED\n\n 304 NOT MODIFIED'
					
				#print(file_content)
			except FileNotFoundError:
				return 'HTTP/1.1 404 NOT FOUND\n\n 404 NOT FOUND'	
	        
	else:
		return 'HTTP/1.1 400 BAD REQUEST\n\n 400 BAD REQUEST'

    			
def threaded(connectionSocket):
	print("Thread id")

	



while True:
	connectionSocket, addr = serverSocket.accept()
	request = connectionSocket.recv(1024).decode()
	connectionSocket.settimeout(2.9)
	print(request.split('\n')[0])
	#with concurrent.futures.ThreadPoolExecutor() as executor:
	#	thread = executor.submit(request)
	#	response = thread.result()
	
	print(response.split('\n')[0])
	connectionSocket.sendall(response.encode())
	connectionSocket.close() 


serverSocket.close()

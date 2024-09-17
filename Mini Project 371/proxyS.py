#Retrieved skeleton code from textbook https://gaia.cs.umass.edu/kurose_ross/programming/Python_code_only/Web_Proxy_programming_only.pdf

from socket import *
import sys

# Create a server socket, bind it to a port and start listening
serverPort = 12000
serverSocket = socket(AF_INET,SOCK_STREAM)

# Fill in start.
serverSocket.bind(('',serverPort))
serverSocket.listen(1)
print('The server is ready to receive')
# Fill in end.

while True:
	# Start receiving data from the client
	tcpCliSock, addr = serverSocket.accept()
	print("Received a connection from:", addr)
	message = tcpCliSock.recv(2048).decode() # Fill in start. # Fill in end.
	print(message)

	# Extract the filename from the given message
	print(message.split()[1])
	filename = message.split()[1].partition("/")[2]
	print(filename)
	fileExist = "false"
	filetouse = "/" + filename
	print(filetouse)
	try:

		# Check wether the file exist in the cache
		f = open(filetouse[1:],"r")
		outputdata = f.readlines()
		#outputdata = bytes(outputdata, "utf-8")
		fileExist= "true"

		# ProxyServer finds a cache hit and generates a response message 
		tcpCliSock.send(bytes("HTTP/1.0 200 OK\r\n",'utf-8'))

		# Fill in start.
		tcpCliSock.send(bytes("Content-Type:text/html\r\n",'utf-8')) 
		for e in range(0, len(outputdata)):
			tcpCliSock.send(bytes(outputdata[e],'utf-8'))

		f.close()
		# Fill in end.

		print('Read from cache')

	except IOError:

		if(fileExist == 'false'):
			# Create a socket on the proxyserver
			c = socket(AF_INET,SOCK_STREAM)
			hostn = filename.replace("www.","",1)
			print(hostn)
			try:
				# Connect to the socket to port 80

				# Fill in start.
				c.connect((hostn,80))
				
				# Create a temporary file on this socket and ask port 80 for the file requested by the client
				fileobj = c.makefile('r',0)
				fileobj.write("GET "+"http://" + filename + "HTTP/1.1\n\n")
				buffer = fileobj.readlines()

				# Create a new file in the cache for the requested file.
				# Also send the response in the buffer to client socket and the corresponding file in the cache

				tmpFile = open("./" + filename,"wb") 
				for e in range(len(buffer)):
					tmpFile.write(buffer[e])
					tcpCliSock.send(buffer[e])
				tmpFile.close()
				print("File from buffer")
			except:
				print("Invalid")
		else:
			#HTTP response message for file not found
			print("File not found")
			

	tcpCliSock.close()

serverSocket.close()


			
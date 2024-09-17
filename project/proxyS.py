from socket import *
import sys

#if len(sys.argv)<=1:
#	print('Usage : "python ProxyServer.py server_ip"\n[server_ip : It is the IP Address Of Proxy Server')
#	sys.exit(2)
serverPort = 12000

# Create a server socket, bind it to a port and start listening
serverSocket = socket(AF_INET,SOCK_STREAM)

# Fill in start.
serverSocket.bind(('',serverPort))
serverSocket.listen(1)
print('The server is ready to receive')
# Fill in end.

while True:
	# Strat receiving data from the client
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
	except FileNotFoundError:
		#HTTP response message for file not found
		print("File not found")
			

	tcpCliSock.close()

serverSocket.close()


			
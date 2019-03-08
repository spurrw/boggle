#!/usr/bin/env python

"""
An echo server that uses select to handle multiple clients at a time.
Entering any line of input at the terminal will exit the server.
"""

import select
import socket
import sys

host = ''
port = 8888
backlog = 5
size = 1024
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host,port))
server.listen(5)
inputList = [server]
running = 1

while running:
    inputready,outputready,exceptready = select.select(inputList,[],[],1)

    for s in inputready:

	#Someone tried to connect to the server for the first time.
	#Let's accept.
        if s == server:
            # handle the server socket
            client, address = server.accept()
            inputList.append(client)
	
	#This is a client sending messages!    
        elif s in inputList:
            # handle all other sockets

	    # try to read
            data = s.recv(size)
            if data:
                print(data.decode().strip())

            else:
                s.close()
                print("Removing a client")
                inputList.remove(s)
                break
            
server.close()

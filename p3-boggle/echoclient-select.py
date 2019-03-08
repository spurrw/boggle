#!/usr/bin/env python

"""
An echo client that allows the user to send multiple lines to the server.
Entering a blank line will exit the client.
"""

import socket
import sys

port = 65311
size = 1024

if len(sys.argv) > 1:
    host = sys.argv[1]
else:
    print("usage: python3 client <hostname>")
    exit()

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((host,port))

while 1:
    # read from keyboard
    try:
        line = input("%")
    except KeyboardInterrupt:
        break
    s.send(bytes(line, 'ascii'))
s.shutdown(socket.SHUT_RDWR)
s.close()

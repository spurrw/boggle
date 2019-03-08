"""
This file contains a couple functions to simplify the sending and receiving
of strings over the network. It's not that necessary, but makes it
a tiny bit easier for me.
Author: William Spurr
"""

"""
Sends a packet on a socket with data: message.
"""
def sendPacket (s, message):
    s.send(bytes(message, 'ascii'))

"""
Recieves a packet and returns the string.
"""
def recvPacket (s):
    return s.recv(4096).decode().strip()

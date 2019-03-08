"""
Boggle game client. It sends strings between it and the Boggle game server.
It prints strings that it gets from the server.
Author: William Spurr
"""

import sys
import socket
import time
import threading

from protocol import *
from network import *


"""
Tries to join the server's game. Returns True
if join succeeded, False if not.
"""
def attemptJoin (s):
    username = sys.argv[3]

    # create join request packet and send
    messageOutgoing = createJoinRequest(username)    
    sendPacket(s, messageOutgoing)

    # wait for reply
    messageReply = recvPacket(s)
    #print(messageReply)
    print(messageText(messageReply)) # print message from server

    # tell whether we are joined
    if isJoinAccepted(messageReply):
        return True
    return False

"""
Thread class that asks for user input and sends it to the server during the
guessing stage 2. A thread is used so the client can listen for the server's
stop message while simultaneously sending.

I used this link to learn how to create a thread: https://www.pythoncentral.io/how-to-create-a-thread-in-python/
"""
class GuessThread (threading.Thread):
    def __init__ (self, _socket):
        threading.Thread.__init__(self)
        self.socket = _socket
        self.sending = True # we set to false when sending time is voer

    def run (self):
        while self.sending:
            guess = input("Enter a guess: ")

            # only send if sending time hasn't expired
                # will still gather user's input later, but won't send it
            if self.sending and len(guess) >= 3:
                sendPacket(self.socket, createGuess(sys.argv[3], guess))

    
"""
Closes the socket and ends the program.
"""
def quit (s):
    s.shutdown(socket.SHUT_RDWR)
    s.close()
    exit()

"""
Main function that is executed on start.
"""
def main ():
    # args checking
    if len(sys.argv) < 4:
        print("usage: python3 client.py <server> <port> <username>")
        exit()

    host = sys.argv[1]
    port = int(sys.argv[2])

    # create socket and connect
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((host, port))

    # try to join game, if can't, quit
    if not attemptJoin(s):
        quit(s)

    playing = True

    guessThread = GuessThread(s)

    # loop for while connected to the server
    while playing:
        message = recvPacket(s)
        if len(message) > 0:
            print(messageText(message) + '\n')

            # Test for different types of messages

            # Case 1: game terminated
            if isGameTerminated(message):
                # send goodbye and quit
                reply = createGoodbye(sys.argv[3])
                sendPacket(s, reply)
                playing = False

            # Case 2: game queued
            elif isGameQueued(message):
                pass # don't really need to do anything here

            # Case 3: game starting
            elif isGameStarting(message):
                guessThread.start()

            elif isGameOver(message):
                # make guessThread not send guesses anymore
                guessThread.sending = False

    
    quit(s)

main()

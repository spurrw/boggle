"""
Boggle game server. This allows connection from up to 4 clients on port 65311 to
play the game of Boggle.
Author: William Spurr
"""

import sys
import socket
import select # magic sauce
import time
import random

from protocol import *
from network import *


"""
Sends a message to all client sockets.
"""
def broadcastClients (playerList, message):
    for p in playerList:
        sendPacket(p[1], message)

"""
Test whether a player should be added to the game. If they should be,
add them.
"""

def tryAddPlayer (message, playerSocket, playerList, stage):
    username = messageUsername(message)

    # joining stage active and not full
    if stage == 1 and len(playerList) < 4:
    # save username with their socket and word guess list
        playerList.append([username, playerSocket, []])

        reply = createJoinAccepted(username)
        sendPacket(playerSocket, reply)
        print(username + " has joined the room.")

        return True

    # return join rejected messages
    elif stage != 1:
        reply = createJoinRejected(username, "Sorry " +\
                username + " but the game is already " +\
                "running. Please try again later.")
        sendPacket(playerSocket, reply)

    else:
        reply = createJoinRejected(username,"Sorry " + username +\
                                    " the game is full already.")

        sendPacket(playerSocket, reply)

    return False

def createBoggleBoard ():
    cubes = [['A', 'A', 'E', 'E', 'G', 'N'], ['A', 'B', 'B', 'J', 'O', 'O'],\
            ['A', 'C', 'H', 'O', 'P', 'S'], ['A', 'F', 'F', 'K', 'P', 'S'],\
            ['A', 'O', 'O', 'T', 'T', 'W'], ['C', 'I', 'M', 'O', 'T', 'U'],\
            ['D', 'E', 'I', 'L', 'R', 'X'], ['D', 'E', 'L', 'R', 'V', 'Y'],\
            ['D', 'I', 'S', 'T', 'T', 'Y'], ['E', 'E', 'G', 'H', 'N', 'W'],\
            ['E', 'E', 'I', 'N', 'S', 'U'], ['E', 'H', 'R', 'T', 'V', 'W'],\
            ['E', 'I', 'O', 'S', 'S', 'T'], ['E', 'L', 'R', 'T', 'T', 'Y'],\
            ['H', 'I', 'M', 'N', 'Q', 'U'], ['H', 'L', 'N', 'N', 'R', 'Z']]
    
    chosenLetters = []
    # choose random cubes and letters
    while len(cubes) > 0:
        cube = random.choice(cubes)
        chosenLetters.append(random.choice(cube))
        cubes.remove(cube)
    
    board = ""
    letterIndex = 0
    for x in range(4):
        for y in range(4):
            board += chosenLetters[letterIndex] + ' '
            letterIndex += 1
        board += '\n'

    return board

"""
Loops through each player's word list and removes any duplicate words.
"""
def removeDuplicateWords (playerList):
    for player in playerList:
        newWordList = []
        for word in player[2]:
            if not word.lower() in newWordList:
                newWordList.append(word.lower())

        player[2] = newWordList

"""
Counts all player scores based on Boggle rules and word length.
Appends scores to each player list in playerList. No words with lenght < 3
will be sent to server, so we don't have to worry about those.
"""
def tabulateScores (playerList):
    for player in playerList:
        score = 0
        for word in player[2]:
            if len(word) == 3 or len(word) == 4:
                score += 1
            elif len(word) == 5:
                score += 2
            elif len(word) == 6:
                score += 3
            elif len(word) == 7:
                score += 5
            else:
                score += 11

        player.append(score)

"""
Formats a message containing info about each client's guesses and their score.
This message is sent to clients later.
"""
def createScoreMessage (playerList):
    message = ""
    # unique words
    for player in playerList:
        message += player[0] + " unique words: "
        
        # remove first word to not follow with a comma
        firstWord = ""
        if len(player[2]) > 0:
            firstWord = player[2][0]
            player[2].remove(firstWord)

        # add other words
        for word in player[2]:
            message += word + ", "

        # add first word to end with no comma
        message += firstWord + '\n'

    # points
    for player in playerList:
        message += player[0] + " points: " + str(player[3]) + '\n'

    # winner (s)
    winners = [playerList[0]]
    for x in range(1, len(playerList)):
        if playerList[x][3] > winners[0][3]:
            winners = [playerList[x]]
        elif playerList[x][3] == winners[0][3]:
            winners.append(playerList[x])
    
    # 1 winner
    if len(winners) == 1:
        message += winners[0][0] + " wins!"
    # multiple winners
    else:
        message += "There is a tie between!: "
        for winner in winners:
            message += winner[0] + ' '

    return message


"""
Main server code. Waits for players in a loop and plays games in a loop.
"""
def main ():
    if len(sys.argv) < 2:
        print("usage: python3 server.py <port>")
        exit()

    host = ''
    port = int(sys.argv[1])
    maxCon = 5
    size = 4096 # max packet size


    # setup server socket on port
    serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    serverSocket.bind((host, port))
    serverSocket.listen(maxCon)
        
    # holds sockets for select
    inputList = [serverSocket]

    # players
    playerList = []

    # server stage
    stage = 1

    # time to be set later when timers are started
    timerEnd = None

    playing = True
    # loop to get input over and over again
    while playing:
        # select, wait for activity on a socket
        inputReady, outputReady, exceptReady = select.select(inputList,[],[],1)

        # timer has expired
        if timerEnd != None and time.time() > timerEnd:
            if stage == 1:
                # start stage 2
                if len(playerList) > 1:
                    replyText = "" + playerList[0][0]
                    for p in playerList[1:]:
                        replyText += " and " + p[0]
                    replyText += " have joined the game. The game " +\
                            "is about to begin."
                    print(replyText)
                    reply = createGameQueued(replyText)
                    broadcastClients(playerList, reply)

                    time.sleep(5) # give a break to get ready

                    stage = 2

                    # create and send board message
                    boardMessage = createBoggleBoard()
                    boardMessage += "\nStart entering words for 3 minutes!"
                    print(boardMessage)
                    boardMessage = createGameStarting(boardMessage)

                    broadcastClients(playerList, boardMessage)

                    # set timer guessing 3 minutes timer
                    timerEnd = time.time() + 180
                
                # not enough players, stopping
                else:
                    replyText = "Not enough players joined, exiting."
                    print(replyText)
                    reply = createGameTerminated(replyText)
                    print(reply)
                    broadcastClients(playerList, reply)

                    # exit
                    playing = False

            elif stage == 2:
                replyText = "\nThe game has ended. Server is tabulating results."
                reply = createGameOver(replyText)
                print(replyText)
                broadcastClients(playerList, reply)

                stage = 3
                # so we don't go in this block again
                timerEnd = None

                # END of game, remove duplicate words, tabulate scores
                    # create and send game results message
                removeDuplicateWords(playerList)
                playerScores = tabulateScores(playerList)
                replyText = createScoreMessage(playerList)
                print(replyText)
                reply = createGameTerminated(replyText)
                broadcastClients(playerList, reply)
                

        # process all active sockets this time around
        for s in inputReady:

            # First time connecting, comes in on serverSocket
            if s == serverSocket:
                client, address = serverSocket.accept()
                # add client socket to those to check for
                inputList.append(client)

            # Client sending messages
            elif s in inputList:
                # read packet data
                data = s.recv(size)
                message = "" # empty for now
                
                # if data was sent, not a termination
                if data:
                    message = data.decode().strip()
                    username = messageUsername(message)
                
                    # case 1: connection request
                    if isJoinRequest(message):
                        # if can't add player, close socket
                        if not tryAddPlayer(message, s, playerList, stage):
                            inputList.remove(s)
                            s.close()

                        # start 1 minute player joining timer
                        elif len(playerList) == 1:
                            timerEnd = time.time() + 60

                    # case 2: guess
                    elif isGuess(message) and stage == 2:
                        word = messageText(message)

                        # add word to correct player
                        for player in playerList:
                            if s in player:
                                player[2].append(word)
                        
                    # case 3: goodbye
                    elif isGoodbye(message):
                        print(messageText(message))
                    
                # client quitting game
                else:
                    print("Removing a client")
                    s.close()
                    inputList.remove(s)
                    # remove play from list too
                    for player in playerList:
                        if s in player:
                            playerList.remove(player)

                    if len(playerList) < 1 and stage == 2:
                        print("No players left, quitting.")
                        playing = False

                    if len(playerList) < 1 and stage == 3:
                        print("exiting")
                        playing = False


                


               

    serverSocket.close()

main()

"""
This file contains functions to work with the Boggle game packet protocol.
It helps with the reading and creation of packets to be sent between client and
server. Mainly, it extracts sections of a packet's data using the protocol I
defined and returns the strings in the packet sections. This file isn't
necessary, but helps me organize functions.
Author: William Spurr
"""

"""
Returns the message section delimeter.
"""
def delimeter ():
    return "?!!?"

"""
Extracts the type of the message, given as a string.
"""
def messageType (string):
    return string[ : string.index(delimeter())]

"""
Extracts the username the message is for / from as a string.
"""
def messageUsername (string):
    startIndex = len(messageType(string)) + len(delimeter())
    return string[startIndex : string.index(delimeter(), startIndex)]

"""
Extracts the text going along with the message as a string.
"""
def messageText (string):
    startIndex = len(messageType(string)) + len(messageUsername(string)) + \
                    2 * len(delimeter())
    return string[startIndex : string.index(delimeter(), startIndex)]




"""
Creates the data for a packet.
"""
def createPacketData (messageType, username, text):
    return messageType + delimeter() + username + delimeter() + text + \
            delimeter()



"""
======== Client to Serve Messages ========
"""

"""
Checks if client is requesting to join.
"""
def isJoinRequest (string):
    if messageType(string) == "join_request":
        return True
    return False

"""
Creates a request to join message.
"""
def createJoinRequest (username):
    return createPacketData("join_request", username, "")

"""
Checks if client is guessing.
"""
def isGuess (string):
    if messageType(string) == "guess":
        return True
    return False

"""
Creates a guess message.
"""
def createGuess (username, text):
    return createPacketData("guess", username, text)

"""
Checks if client is saying goodbye.
"""
def isGoodbye (string):
    if messageType(string) == "goodbye":
        return True
    return False

"""
Creates a goodbye message.
"""
def createGoodbye (username):
    return createPacketData("goodbye", username, "Goodbye, server. Love, " + \
                            username + " <3")

"""
======== Server to Client Messages ========

"""

"""
Checks if the server accepted the clients join.
"""
def isJoinAccepted (string):
    if messageType(string) == "join_accepted":
        return True
    return False

"""
Creates a join accepted packet message.
"""
def createJoinAccepted (username):
    return createPacketData("join_accepted", username, "Welcome to the game, " \
                                + username + ". Waiting for others to join.")
"""
Checks if the server rejects the clients join.
"""
def isJoinRejected (string):
    if messageType(string) == "join_rejected":
        return True
    return False

"""
Creates a join rejected packet message.
"""
def createJoinRejected (username, text):
    #print(createPacketData("join_rejected", username, text))
    return createPacketData("join_rejected", username, text)


"""
Checks if a game terminated message was sent.
"""
def isGameTerminated (string):
    if messageType(string) == "game_terminated":
        return True
    return False

"""
Creates a terminated message.
"""
def createGameTerminated (text):
    #print(createPacketData("game_terminated", "", text))
    return createPacketData("game_terminated", "all", text)

"""
checks if the server is about to start the game.
"""
def isGameQueued (string):
    if messageType(string) == "game_queued":
        return True
    return False

"""
creates a game is queued message.
"""
def createGameQueued (text):
    #print(createpacketdata("game_queued", "", text))
    return createPacketData("game_queued", "all", text)


"""
checks if the server is starting the game.
"""
def isGameStarting (string):
    if messageType(string) == "game_starting":
        return True
    return False

"""
creates a game is queued message.
"""
def createGameStarting (text):
    #print(createpacketdata("game_queued", "", text))
    return createPacketData("game_starting", "all", text)


"""
checks if game is over
"""
def isGameOver (string):
    if messageType(string) == "game_over":
        return True
    return False

"""
create a game is over message.
"""
def createGameOver (text):
    return createPacketData("game_over", "all", text)

"""
checks if game is terminated
"""
def isGameTerminated (string):
    if messageType(string) == "game_terminated":
        return True
    return False

"""
create a game is terminated message
"""
def createGameTerminated (text):
    return createPacketData("game_terminated", "all", text)

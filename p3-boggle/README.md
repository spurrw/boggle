readme.txt for Boggle Python implementation by William Spurr
no group members

====== 1. Running Instructions

=== A. Server
    The following files are needed to run the Boggle server:
    server.py
    protocol.py
    network.py
    
    Run server with: python3 server.py <port>
    
=== B. Client
    The following files are needed to run the Boggle client:
    client.py
    protocol.py
    network.py
    
    Run client with: python3 client.py <server addr> <server port> <username>

====== 2. External Sources and Challenges

	I encountered one large challenge in this project where I needed
to consult outside sources for. I got stuck when coding the client to be able
to send unlimited guesses to the server for 3 minutes. I know I could write
a loop that would end after 3 minutes, but what if 3 minutes ended while the
python function input() was waiting for the user to hit enter? The loop wouldn't
end before that, meanwhile the program wouldn't be receiving packets from the
server telling it that the game was over. It would be stuck in a loop like the
following:

while timeElapsed < 3 minutes:
    guess = input("Enter a word guess: ")
    sendPacketToServer(guess)
    
    I needed a way to be able to end this loop of listening for user input while
input() was being called. I also didn't want to rely on the client to keep track
of time, but have the client listen for a server packet telling it that it can't
guess anymore. That way, it is easy to change the timing of the game, and just
seems cleaner. I experimented with signal alarms, but decided another thread
was needed. My client code would have to wait for user input while listening
for a packet from the server telling it the guessing period had ended. I
consulted the following webpage to lookup how to create another thread in
python.

https://www.pythoncentral.io/how-to-create-a-thr

    Now, my client starts another thread which enters a loop of waiting for
user input and sending a guess to the server. While this thread is running the
main function is still able to listen for the server to signal that the guessing
stage is over. Unfortunately, when the game is over, the client code still
requires a Ctrl+C to quit, which throws an exception because the thread is still
running and waiting for user input.

    Other than this I didn't have any major difficulties to speak of.

====== 3. Example Working Gameplay

=== A. Server Screen:
spurrw@jalad:~/p3-boggle$ python3 server.py 65311
Will has joined the room.
Kaycee has joined the room.
Will and Kaycee have joined the game. The game is about to begin.
D V N S 
R O C O 
Y T O U 
R J E Q 

Start entering words for 3 minutes!

The game has ended. Server is tabulating results.
Will unique words: dot, rot, don, son, not
Kaycee unique words: not, rot, quote, roy, vote, tod
Will points: 5
Kaycee points: 7
Kaycee wins!
Goodbye, server. Love, Will <3
Removing a client
Goodbye, server. Love, Kaycee <3
Removing a client
exiting

=== B. Client 'Will' Screen:
will@venus:~/Documents/Networking/p3-boggle$ python3 client.py student.cs.uni.edu 65311 Will
Welcome to the game, Will. Waiting for others to join.
Will and Kaycee have joined the game. The game is about to begin.

D V N S 
R O C O 
Y T O U 
R J E Q 

Start entering words for 3 minutes!

Enter a guess: not
Enter a guess: dot
Enter a guess: rot
Enter a guess: don
Enter a guess: Son 
Enter a guess: 
The game has ended. Server is tabulating results.

Will unique words: dot, rot, don, son, not
Kaycee unique words: not, rot, quote, roy, vote, tod
Will points: 5
Kaycee points: 7
Kaycee wins!

=== C. Client 'Kaycee' Screen:
will@venus:~/Documents/Networking/p3-boggle$ python3 client.py student.cs.uni.edu 65311 Kaycee
Welcome to the game, Kaycee. Waiting for others to join.
Will and Kaycee have joined the game. The game is about to begin.

D V N S 
R O C O 
Y T O U 
R J E Q 

Start entering words for 3 minutes!

Enter a guess: tod
Enter a guess: not
Enter a guess: rot
Enter a guess: quote
Enter a guess: roy
Enter a guess: vote
Enter a guess: 
The game has ended. Server is tabulating results.

Will unique words: dot, rot, don, son, not
Kaycee unique words: not, rot, quote, roy, vote, tod
Will points: 5
Kaycee points: 7
Kaycee wins!


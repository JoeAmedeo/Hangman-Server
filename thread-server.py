"""
Server side: open a socket on a port, listen for a message from a client,
and send an echo reply; echoes lines until eof when client closes socket;
spawns a thread to handle each client connection; threads share global
memory space with main thread; this is more portable than fork: threads
work on standard Windows systems, but process forks do not;
"""

import time, _thread as thread           # or use threading.Thread().start()
from socket import *                     # get socket constructor and constants
import random

myHost = ''                              # server machine, '' means local host
myPort = 50007                           # listen on a non-reserved port number

sockobj = socket(AF_INET, SOCK_STREAM)           # make a TCP socket object
sockobj.bind((myHost, myPort))                   # bind it to server port number
sockobj.listen(5)                                # allow up to 5 pending connects

def now():
    return time.ctime(time.time())               # current time on the server

def handleClient(connection):                    # in spawned thread: reply
    time.sleep(5)                                # simulate a blocking activity
   # while True:                                  # read, write a client socket
        #data = connection.recv(1024)
        #if not data: break
        #reply = 'Echo=>%s at %s' % (data, now())
        #connection.send(reply.encode())
    #connection.close()

    HANGMAN = (
        """
         ------
         |    |
         |
         |
         |
         |
         |
         |
         |
        ----------
        """,
        """
         ------
         |    |
         |    O
         |
         |
         |
         |
         |
         |
        ----------
        """,
        """
         ------
         |    |
         |    O
         |   -+-
         |
         |
         |
         |
         |
        ----------
        """,
        """
         ------
         |    |
         |    O
         |  /-+-
         |
         |
         |
         |
         |
        ----------
        """,
        """
         ------
         |    |
         |    O
         |  /-+-/
         |
         |
         |
         |
         |
        ----------
        """,
        """
         ------
         |    |
         |    O
         |  /-+-/
         |    |
         |
         |
         |
         |
        ----------
        """,
        """
         ------
         |    |
         |    O
         |  /-+-/
         |    |
         |    |
         |   |
         |   |
         |
        ----------
        """,
        """
         ------
         |    |
         |    O
         |  /-+-/
         |    |
         |    |
         |   | |
         |   | |
         |
        ----------
        """)

    """in order to a get a broader list of options for words to play with in hangman,
    We will traverse the given txt file and put all words into a very large list """

    textFile = open('newWordList.txt', 'r')     #open list of words
    WORDS = []                                  #initialize array
    for line in textFile:                       #put all word in txt file into an array
        WORDS.append(line.upper())

    textFile.close()

    MAX_WRONG = len(HANGMAN) - 1

    # initialize variables
    word = random.choice(WORDS)  # the word to be guessed
    so_far = "-" * len(word)  # one dash for each letter in word to be guessed
    wrong = 0  # number of wrong guesses player has made
    used = []  # letters already guessed

    connection.send("Welcome to Hangman.  Good luck!".encode())

    while wrong < MAX_WRONG and so_far != word:
        #isConnected = "0"           #initialize key, as long as it is true keep connection open
        encoded_used = ""           #initialize variables
        for x in used:
            encoded_used = encoded_used + x         #get all used letters into one variable to encode and send
        send_content = HANGMAN[wrong].encode() + "\nYou've used the following letters:\n".encode() + encoded_used.encode() + "\nSo far, the word is:\n".encode() + so_far.encode()      #take all the content that was printed in the original hangman file and send it over the socket
        connection.send(send_content)       #send the content
        #connection.send(isConnected.encode())       #send connection variable

        guess = connection.recv(1024)       #recieve guess from client
        guess = guess.decode()              #decode message
        guess = guess.upper()               #make upper case

        if guess in used:
            connection.send("You've already guessed the letter ".encode() + guess.encode())         #tell user they already guessed the letter

        elif guess in word:
            used.append(guess)      #add guess to the list
            connection.send("\nYes!".encode() + guess.encode() + " is in the word!".encode())       #tell user they guessed a letter in the word

            # create a new so_far to include guess
            new = ""
            for i in range(len(word)):
                if guess == word[i]:
                    new += guess
                else:
                    new += so_far[i]
            so_far = new

        else:
            used.append(guess)      #add word to list
            connection.send("\nSorry,".encode() + guess.encode() + "isn't in the word.".encode())   #tell user their guess was wrong
            wrong += 1              #increment wrong counter

    if wrong == MAX_WRONG:
        connection.send(HANGMAN[wrong].encode() + "\nYou've been hanged!".encode())         #send message for losing the game
    else:
        connection.send("\nYou guessed it!".encode())                                       #send message for winning the game

    connection.send("\nThe word was ".encode() + word.encode() + "\n\nType in any letter to exit".encode())         #closing message


    connection.close()


def dispatcher():                                # listen until process killed
    while True:                                  # wait for next connection,
        connection, address = sockobj.accept()   # pass to thread for service
        print('Server connected by', address, end=' ')
        print('at', now())
        thread.start_new_thread(handleClient, (connection,))

dispatcher()

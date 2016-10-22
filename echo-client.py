"""
Client side: use sockets to send data to the server, and print server's
reply to each message line; 'localhost' means that the server is running
on the same machine as the client, which lets us test client and server
on one machine;  to test over the Internet, run a server on a remote
machine, and set serverHost or argv[1] to machine's domain name or IP addr;
Python sockets are a portable BSD socket interface, with object methods
for the standard socket calls available in the system's C library;
"""

import sys
from socket import *              # portable socket interface plus constants
import time
serverHost = 'localhost'          # server name, or: 'starship.python.net'
serverPort = 50007                # non-reserved port used by the server

message = []         # default text to send to server
                                            # requires bytes: b'' or str,encode()
if len(sys.argv) > 1:       
    serverHost = sys.argv[1]                # server from cmd line arg 1
    if len(sys.argv) > 2:                   # text from cmd line args 2..n
        message = (x.encode() for x in sys.argv[2:])  

sockobj = socket(AF_INET, SOCK_STREAM)      # make a TCP/IP socket object
sockobj.connect((serverHost, serverPort))   # connect to server machine + port

for line in message:
    sockobj.send(line)                      # send line to server over socket
    data = sockobj.recv(1024)               # receive line from server: up to 1k
    print('Client received:', data)         # bytes are quoted, was `x`, repr(x)

data = sockobj.recv(1024).decode()          #recieve and print welcome message
print(data)

isConnected = True

while isConnected:

    data= sockobj.recv(1024).decode()               #recieve initial message from server, includes hangman image, letters guessed, and the word discovered so far

    print(data)                                     #print message



    guess = input('\n\nEnter your guess here: ')    #have the user input their guess
    sockobj.send(guess.encode())                    #send guess to server


    line1 = sockobj.recv(1024)                      #recieve response from server
    if len(line1) == 0:
        isConnected = False                         #if the response length is zero, the connection no longer exists
    else:
        print(line1.decode())                       #print response


sockobj.close()                             # close socket to send eof to server

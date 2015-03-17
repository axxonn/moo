#!/usr/bin/env python

import argparse
import random
import socket
import SocketServer

parser = argparse.ArgumentParser()
parser.add_argument("number", help="the secret number")
parser.add_argument("my_port", help="the player's port")
args = parser.parse_args()
chosen = args.number

def is_valid(num):
 digits = '123456789'
 return len(num) == 4 and \
  all(char in digits for char in num) \
  and len(set(num)) == 4

won = False

class MyUDPHandler(SocketServer.BaseRequestHandler):
    def handle(self):
        data = self.request[0].strip()
        socket = self.request[1]
        raw = data.split(':')
        if (raw[0] != 'GUESS'):
           socket.sendto('BAD FORMAT', self.client_address)
           return        
        guess = raw[1].strip()
        if not is_valid(guess):
         socket.sendto('BAD NUMBER', self.client_address) 
        if int(guess) == int(chosen):
         socket.sendto('WIN', self.client_address)
	 global won
         won = True
         return
        bulls = cows = 0
        for i in range(4):
         if guess[i] == chosen[i]:
            bulls += 1
         elif guess[i] in chosen:
            cows += 1
        socket.sendto('%iB%iC' % (bulls, cows), self.client_address) 


HOST, PORT = "localhost", int(args.my_port)

def client():
 sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
 sock.settimeout(1)
 for a in range(1, 10):
    for b in range(1, 10):
     for c in range(1, 10):
      for d in range(1, 10):
       if len(set([a,b,c,d])) < 4:
        continue
       myguess = ''.join(map(str, [a, b, c, d]))
       sock.sendto('GUESS:' + myguess, (HOST, PORT))
       received = sock.recv(1024)
       print "Guessed:  " + str(myguess)
       print "Received: {}\n".format(received)
       if "{}".format(received) == 'WIN':
        return

def server():
 if not is_valid(chosen):
  print 'SECRET IS NOT VALID'
  return
 server = SocketServer.UDPServer((HOST, PORT), MyUDPHandler)
 while not won:
  server.handle_request()

try:
 client() 
except socket.timeout:
 server()

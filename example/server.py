# first of all import the socket library
import socket
import random

# next create a socket object
sk = socket.socket()
print ("Socket successfully created")

# reserve a port on your computer in our
# case it is 12345 but it can be anything
port = 30081

# Next bind to the port
# we have not typed any ip in the ip field
# instead we have inputted an empty string
# this makes the server listen to requests
# coming from other computers on the network
sk.bind(("127.0.0.1", 30081))
print ("socket binded to %s" % (port))

# put the socket into listening mode
sk.listen(5)
print ("socket is listening")

# a forever loop until we interrupt it or
# an error occurs
while True:

  # Establish connection with client.
  server, address = sk.accept()
  print ('Got connection from', address)

  # send a thank you message to the client.
  server.send('Thank you for connecting')
  msg = "Welcome to Socket World"
  server.send(msg.encode())
  while True:
    data = server.recv(1024) # Receive Client message
    print(data.decode()) # Print the data receive
    if data == b'exit':
      break
    server.send(data.encode()) # handle the data from client
    server.send(str(random.randint(1,300)).encode()) # Send the random data

   # Close the connection with the client
    server.close()

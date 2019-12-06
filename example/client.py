 # Import socket module 
import socket                
  
# Create a socket object 
client = socket.socket()          
  
# Define the port on which you want to connect 
port = ("127.0.0.1", 30081)
client.connect(port)
  
while True: 
  # receive data from the server 
  data = client.recv(1024)  
  print (data.decode()) # Print the data receive

  msg_input = input("Please input data >> ")
  client.send(msg_input.encode())
  if msg_input == 'exit':
    break

  data = client.recv(1024)
  print(data.decode)
  # close the connection 
  client.close()   
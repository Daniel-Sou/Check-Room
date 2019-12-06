# file_server2.py
from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread
import os
from enum import Enum

# from SocketServer import ThreadingMixIn

TCP_IP = ''
TCP_PORT = 9001
clients = {}
addresses = {}
BUF_SIZ = 1024
file_list = []


class CmdType(Enum):
    Command = '-c'
    Quit = '-q'
    CheckFile = '-cf'
    DownloadFile = '-df'
    UploadFile = '-up'


def accept_incoming_connections():
    """Sets up handling for incoming clients."""
    while True:
        client, client_address = SERVER.accept()
        print("%s:%s has connected." % client_address)
        client.send(bytes("System : Greetings from the cave! Now type your name and press enter!", "utf8"))
        addresses[client] = client_address
        Thread(target=handle_client, args=(client,)).start()


def handle_client(client):  # Takes client socket as argument.
    """Handles a single client connection."""

    name = client.recv(BUF_SIZ).decode("utf8")
    welcome = 'System : Welcome %s! Type "-c" to check command.' % name
    client.send(bytes(welcome, "utf8"))
    msg = "%s has joined the chat!" % name
    broadcast(bytes(msg, "utf8"))
    clients[client] = name
    if not file_list:
        append_file_list()

    while True:
        try:
            msg = client.recv(BUF_SIZ)
            if msg == bytes(CmdType.Command.value, "utf8"):
                client.send(bytes("The command as following :\n" +
                                  "Quit : -q\n" +
                                  "CheckFile : -cf\n" +
                                  "DownloadFile : -df\n" +
                                  "UploadFile : select the button 'select file'", "utf8"))

            elif msg == bytes(CmdType.Quit.value, "utf8"):
                client.send(bytes("{quit}", "utf8"))
                client.close()
                del clients[client]
                broadcast(bytes("%s has left the chat." % name, "utf8"))
                break

            elif msg == bytes(CmdType.CheckFile.value, "utf8"):
                check_file_list(client)

            elif msg == bytes(CmdType.UploadFile.value, "utf8"):
                file_name = client.recv(BUFSIZE).decode("utf8")
                file_content = client.recv(BUFSIZE).decode("utf8")
                if upload_file(file_name, file_content, client):
                    client.send(bytes("Upload file success", "utf8"))
                else:
                    client.send(bytes("Upload file Fail", "utf8"))

            elif msg == bytes(CmdType.DownloadFile.value, "utf8"):
                client.send(bytes("Please select your file num(0, 1, 2, 3...) : ", "utf8"))
                check_file_list(client)
                result = check_int(client.recv(BUF_SIZ).decode("utf8"), client)
                if result is not None:
                    download_file(result, client)
                    client.send(bytes("Download success", "utf8"))

            else:
                broadcast(msg, name + ": ")
        except ConnectionResetError:
            client.close()
            del clients[client]
            broadcast(bytes("%s has left the chat." % name, "utf8"))
            continue
        except OSError:
            continue


def broadcast(msg, prefix=""):  # prefix is for name identification.
    """Broadcasts a message to all the clients."""

    for sock in clients:
        sock.send(bytes(prefix, "utf8") + msg)


def append_file_list():
    """The support function of handle the files save in server."""
    if not os.path.isfile('./server_file/filelist.txt'):
        file = open("./server_file/filelist.txt", "w+")
        file.close()

    with open("./server_file/filelist.txt", "r") as fr:
        for line in fr.readlines():
            terms = line.rstrip().split()
            file_list.append(terms[0])


def check_file_list(client):
    """Send exists file in the server to client"""
    if not file_list:
        client.send(bytes("No file in server", "utf8"))
    else:
        client.send(bytes("File list is: ", "utf8"))
        content = ""
        for i in range(len(file_list)):
            content += str(i) + ". " + str(file_list[i]) + "\n"
        client.send(bytes(content, "utf8"))


def upload_file(name, content, client):
    """Save the file from client"""
    print(name)
    if name in file_list:
        client.send(bytes("The file has same name with other file in file server,\n do you want overwrite (reply 'a') "
                          "it or change the file name? (reply 'b')", "utf8"))
        reply = client.recv(BUFSIZE).decode("utf8")
        if reply == 'a':
            os.remove("./server_file/" + str(file_list.pop(file_list.index(name))))
        elif reply == 'b':
            client.send(bytes("Please enter the new file name:", "utf8"))
            filename = client.recv(BUFSIZE).decode("utf8") + ".txt"
            upload_file(filename, content, client)
        else:
            return False

    elif len(file_list) >= 5:
        os.remove("./server_file/" + str(file_list.pop(0)))

    file_list.append(name)
    file = open("./server_file/" + name, "w+")
    file.write(content)
    file.close()

    with open("./server_file/filelist.txt", "w") as fr:
        for file_name in file_list:
            fr.write(file_name + "\n")

    return True


def download_file(num, client):
    """Send selected file to client"""
    client.send(bytes("{download_file}", "utf8"))
    filename = file_list[int(num)]
    client.send(bytes(filename, "utf8"))
    content = ""
    with open("./server_file/" + filename, "r") as fr:
        for line in fr.readlines():
            content += line
    client.send(bytes(content, "utf8"))


def check_int(s, client):
    """Check the input value is int"""
    try:
        s = int(s)
        if len(file_list) > s >= 0:
            return s
        else:
            client.send(bytes("Error : out of file range", "utf8"))
            return None
    except ValueError:
        client.send(bytes("Error : input type incorrect", "utf8"))
        return None


HOST = ''
# The server should be able to set the port it will listen
PORT = input('Enter port: ')
if not PORT:
    PORT = 33000
else:
    PORT = int(PORT)

BUFSIZE = 1024

#
SERVER = socket(AF_INET, SOCK_STREAM)
SERVER.bind((HOST, PORT))

if __name__ == "__main__":
    # The server should be able to handle multiple clients
    SERVER.listen(5)
    print("Waiting for connection...")
    ACCEPT_THREAD = Thread(target=accept_incoming_connections)
    ACCEPT_THREAD.start()
    ACCEPT_THREAD.join()

SERVER.close()

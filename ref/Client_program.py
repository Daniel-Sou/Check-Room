#!/usr/bin/env python3
"""Script for Tkinter GUI chat client."""
from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread
import tkinter
from tkinter import filedialog
import os
from pip._vendor.msgpack.fallback import xrange


def receive():
    """Handles receiving of messages."""
    while True:
        try:
            msg = client_socket.recv(BUFSIZ).decode("utf8")
            if msg == "{download_file}":
                filename = client_socket.recv(BUFSIZ).decode("utf8")
                content = client_socket.recv(BUFSIZ).decode("utf8")
                with open(filename, "w") as fr:
                    fr.write(content)
            else:
                if "\n" in msg:  # D
                    while True:
                        for i in xrange(len(msg)):
                            if "\n" == msg[i:i + len("\n")]:
                                msg_list.insert(tkinter.END, msg[:i])
                                msg = msg[i + len("\n"):]
                                break
                        if "\n" not in msg:
                            msg_list.insert(tkinter.END, msg)
                            break
                else:
                    msg_list.insert(tkinter.END, msg)
        except OSError:  # Possibly client has left the chat.
            break


def send(event=None):  # event is passed by binders.
    """Handles sending of messages."""
    msg = my_msg.get()
    my_msg.set("")  # Clears input field.
    client_socket.send(bytes(msg, "utf8"))
    if msg == "{quit}":
        client_socket.close()
        top.quit()


def on_closing(event=None):
    """This function is to be called when the window is closed."""
    my_msg.set("{quit}")
    send()


def find_file():
    """Find the file in computer and send it via the server."""
    file_path = filedialog.askopenfilename(initialdir="/", title="Select file",
                                           filetypes=(("Txt file", "*.txt"), ("all file", "*.*")))
    filename = os.path.join(os.path.dirname(os.path.realpath('__file__')), file_path)
    content = ""
    with open(filename, "r") as fr:
        for line in fr.readlines():
            content += line
    my_msg.set("-up")
    send()
    my_msg.set(os.path.basename(file_path))
    send()
    my_msg.set(content)
    send()


top = tkinter.Tk()
top.title("Chatter")

messages_frame = tkinter.Frame(top)
my_msg = tkinter.StringVar()  # For the messages to be sent.
my_msg.set("Type your messages here.")
scrollbar = tkinter.Scrollbar(messages_frame)  # To navigate through past messages.
# Following will contain the messages.
msg_list = tkinter.Listbox(messages_frame, height=15, width=50, yscrollcommand=scrollbar.set)
scrollbar.pack(side=tkinter.RIGHT, fill=tkinter.Y)
msg_list.pack(side=tkinter.LEFT, fill=tkinter.BOTH)
msg_list.pack()
messages_frame.pack()

entry_field = tkinter.Entry(top, textvariable=my_msg)
entry_field.bind("<Return>", send)
entry_field.pack()

send_button = tkinter.Button(top, text="Send", command=send)
send_button.pack()

send_file_button = tkinter.Button(top, text="Select file", command=find_file)
send_file_button.pack()

top.protocol("WM_DELETE_WINDOW", on_closing)

# ----Now comes the sockets part----
HOST = input('Enter host: ')
PORT = input('Enter port: ')
if not PORT:
    PORT = 33000
else:
    PORT = int(PORT)

BUFSIZ = 1024

client_socket = socket(AF_INET, SOCK_STREAM)
client_socket.connect((HOST, PORT))

receive_thread = Thread(target=receive)
receive_thread.start()
tkinter.mainloop()  # Starts GUI execution.

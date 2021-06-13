import socket
import threading
import memory

NICK = "venomega"
USER = ""


def the_reader():
    object = memory.object
    while memory.status:
        buff = object.recv(3333)
        print(buff, flush=True)


o = socket.socket()  # create socket
o.connect(("irc.ea.libera.chat", 6667))  # connect to server
memory.object = o  # share the object through memory


threading.Thread(target=the_reader).start()  # inint the receiver engine

# send initial msgs
o.send(
    f"NICK {NICK}\nUSER venomega venomega_ venomega__ :Ernest Brown\n".encode())

input()
memory.status = False

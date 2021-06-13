from curses import wrapper
import win
import socket
import threading
import memory
import sys
import time

NICK = "venomega"
USER = "Ernest Brown"


def connect(NICK, USER):
    o = socket.socket()  # create socket
    o.connect(("irc.ea.libera.chat", 6667))  # connect to server
    memory.object = o  # share the object through memory

    threading.Thread(target=the_reader).start()  # inint the receiver engine

    # send initial msgs
    o.send(
        f"NICK {NICK}\nUSER {NICK} {NICK}_ {NICK}__ :{USER}\n".encode())
    time.sleep(7)
    print("NOW", flush=True)
    o.send("JOIN #lobby\n".encode())


def the_reader():
    while memory.status:
        buff = memory.object.recv(8000)
        recv = buff.decode()
        if recv.split()[1] in ["NOTICE", "PRIVMSG"]:
            token = recv.split(':')[2:]
            buffer = ""
            buffer += "<" + recv.split()[0].split("!")[0][1:] + "> "
            for i in token:
                for x in i:
                    if not x == "\n":
                        buffer += x
            memory.window.buffer_add(buffer)
        if "PING" in recv:
            memory.object.send(f"PONG {recv.split()[-1]}\n".encode())


def screen(stdscr):
    global NICK, USER
    memory.window = win.window(0.99, 0.99, 0.01, 0.01)
    memory.window.build()
    connect(NICK, USER)
    while True:
        memory.window.write_buffer()
        time.sleep(1)


wrapper(screen)

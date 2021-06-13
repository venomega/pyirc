from curses import wrapper
import curses
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
                        if len(buffer) >= (memory.screen_width - 2):
                            memory.window.buffer_add(buffer)
                            buffer = ""

                        buffer += x
            memory.window.buffer_add(buffer)
        if "PING" in recv:
            memory.object.send(f"PONG {recv.split()[-1]}\n".encode())


def screen_loop():
    while True:
        memory.window.write_buffer()
        time.sleep(1)


def screen(stdscr):
    global NICK, USER
    memory.screen_width = curses.COLS - 2
    memory.window = win.window(0.90, 0.99, 0.01, 0.01)
    memory.window.build()
    connect(NICK, USER)
    threading.Thread(target=screen_loop).start()

    o = win.window(0.1, 0.99, 0.9, 0.01)
    o.build(1)
    num = 200
    buffer = ""
    while True:
        asd = o.win.getch()

        if asd == 10:  # enter has pressed
            if len(buffer) > 0:
                memory.object.send(f"{buffer}\n".encode())
                buffer = ""
        if asd in [8, 127]:  # backspace
            buffer = buffer[:-1]
        if num - len(buffer) <= 0:
            continue
        if asd >= 97 and asd <= 122:  # lower keys
            buffer += asd.to_bytes(1, 'little').decode()
        if asd >= 65 and asd <= 90:  # upper keys
            buffer += asd.to_bytes(1, 'little').decode()
        if asd == 32:  # space bar
            buffer += asd.to_bytes(1, 'little').decode()
        if asd == 35:  # hastag
            buffer += asd.to_bytes(1, 'little').decode()

        o.write(0, 0, " " * (memory.screen_width))
        if len(buffer) > memory.screen_width:
            o.write(0, 0, buffer[eval(f"-{memory.screen_width - 1}"):])
        else:
            o.write(0, 0, buffer)
        o.write(1, 0, f"{num-len(buffer)}")


wrapper(screen)

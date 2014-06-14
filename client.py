#!/usr/bin/python
#
# Basic python client
# Taken from http://www.tutorialspoint.com/python/python_networking.htm
# June 12, 2014

import socket as so
import time
import sys

class Connection:
    def __enter__(self):
        """
        Stole most of the skeleton of this code from http://oreilly.com/pub/h/1968
        """

        self.nick = 'BadMuthaUcka'
        port = 6667
        address = 'irc.freenode.net'

        s = so.socket()
        s.connect((address,port))
        self.s = s

        return self

    def join_server(self):
        s = self.s
        nick = self.nick
        s.send("CAP LS\r\n")

        channel = '#humptydumpty'

        running = True

        while running:
            # Replace this with a receive func
            readbuffer = ''
            readbuffer = readbuffer+s.recv(1024)
            temp = readbuffer.split("\n")
            readbuffer = temp.pop()

            for line in temp:
                line = line.rstrip()
                line = line.split()
                print line
                if len(line) < 2:
                    break

                if line[0]=="PING":
                    s.send("PONG %s\r\n" % line[1])

                if line[1]=="CAP":
                    if line[3]=="LS" and "multi-prefix" in line[3:]:
                        s.send("CAP REQ multi-prefix\r\n")
                        s.send("CAP END\r\n")
                        s.send("NICK %s\r\n" % nick)
                        s.send("USER %s %s bla :%s\r\n" % ("badmutha", "*", "*"))

                if line[1]=="376":
                    s.send(''.join(['JOIN ',channel,'\r\n']))
                    time.sleep(10)
                    self.depart_room(channel)
                    self.leave_server()
                    running = False

    def leave_server(self):
        self.buffered_send('QUIT\r\n')

    def buffered_send(self,msg):
        # TODO: Actually write this function
        self.s.send(msg)

    def depart_room(self,channel,goodbye=''):
        # TODO: Multiple channel quit
        cmd = ['PART ']
        cmd.append(channel)
        if goodbye != '':
            bye = ''.join([':',goodbye])
            cmd.append(bye)
        cmd.append('\r\n')
        self.buffered_send(''.join(cmd))

    def __exit__(self, type, value, traceback):
        self.s.close()

def main():
    print "huh?"

if __name__=="__main__":
    main()

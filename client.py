#!/usr/bin/python
#
# Basic python client
# Taken from http://www.tutorialspoint.com/python/python_networking.htm
# June 12, 2014

import socket as so
import time
import sys
import Queue


class Connection:

    def __init__(self):
        """
        Stole most of the skeleton of this code from http://oreilly.com/pub/h/1968
        """

        self.nick = 'BadMuthaUcka'
        self.channel = '#humptydumpty'

        self.stack = Queue.Queue()
        self.stack.put((self.server_connect,('irc.freenode.net',6667)))

        self.s = so.socket()

        temp = ''

        while self.select(temp) > 0:
            temp = self.receive(1024)

    def server_connect(self,addrTuple):
        print 'server connecting'
        self.s.connect(addrTuple)
        self.s.send('CAP LS\r\n')

    def receive(self,size):
            readbuffer = ''
            readbuffer = readbuffer + self.s.recv(size)
            temp = readbuffer.split("\n")
            readbuffer = temp.pop()
            return temp

    def passMessage(self):
        if self.stack.empty():
            return
        else:
            t = self.stack.get()
            f = t[0]
            arg = t[1]
            return f(arg)

    def select(self,temp):
        self.passMessage()
        for line in temp:
            line = line.rstrip()
            line = line.split()
            print line

            if line[0]=="PING":
                self.s.send("PONG %s\r\n" % line[1])

            if line[1]=="CAP":
                if line[3]=="LS" and "multi-prefix" in line[3:]:
                    self.s.send("CAP REQ multi-prefix\r\n")
                    self.s.send("CAP END\r\n")
                    self.s.send("NICK %s\r\n" % self.nick)
                    self.s.send("USER %s %s bla :%s\r\n" % ("badmutha", "*", "*"))

            # This will be replaced by input
            if line[1]=="376":
                print "SERVER CONNECTION ESTABLISHED. ALL MESSAGES RECEIVED."
                self.join_channel('#humptydumpty')
            
            # This will be replaced by input
            if line[1]=="JOIN":
                self.privmsg('Hwhaddup playaaaa')

        return 1

    def join_channel(self,chan):
        print 'joining channel'
        self.channel = chan
        self.s.send(''.join(['JOIN ',chan,'\r\n']))

    def privmsg(self, msg):
        a = ''.join(['PRIVMSG ', self.channel, ' :', msg, '\r\n'])
        print a
        self.buffered_send(a)

    def topic_change(self, topic):
        self.buffered_send(''.join(['TOPIC', self.channel, topic]))

    def leave_server(self):
        self.buffered_send('QUIT\r\n')

    def buffered_send(self,msg):
        # TODO: Actually write this function
        self.s.send(msg)

    def depart_room(self,channel,goodbye=''):
        # TODO: Multiple channel quit (multiple channel everything)
        cmd = ['PART ']
        cmd.append(channel)
        if goodbye != '':
            bye = ''.join([':',goodbye])
            cmd.append(bye)
        cmd.append('\r\n')
        self.buffered_send(''.join(cmd))

    def __exit__(self, type, value, traceback):
        self.s.close()
        return 0

def main():
    print "huh?"

if __name__=="__main__":
    main()

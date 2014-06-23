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

    def __init__(self,nick,channel=None):
        """
        Stole most of the skeleton of this code from http://oreilly.com/pub/h/1968
        """

        self.nick = nick 
        if channel!= None:
            self.channel = channel
        self.stack = Queue.Queue()
        self.stack.put((self.server_connect,('irc.freenode.net',6667)))
        self.s = so.socket()

        rb = ''
        temp = ''

        while self.run(temp) > 0:
            rb, temp = self.receive(rb,1024)

    def server_connect(self,addrTuple):
        self.s.connect(addrTuple)
        self.buffered_send('CAP LS\r\n')

    def receive(self,readbuffer,size):
        try:
            readbuffer = readbuffer + self.s.recv(size)
            temp = readbuffer.split("\n")
            readbuffer = temp.pop()
            return readbuffer, temp
        except (KeyboardInterrupt, SystemExit):
            print 'Closing socket\n'
            self.leave_channel(self.channel, 'See ya suckers!')
            self.leave_server()
            self.s.close()
            raise

    def passMessage(self):
        if self.stack.empty():
            return
        else:
            t = self.stack.get()
            f = t[0]
            arg = t[1]
            return f(arg)

    def run(self,temp):
        self.passMessage()
        for line in temp:
            line = line.rstrip()
            line = line.split()
            print line

            # Put here all things that need to be responded to.
            if line[0]=="PING":
                self.buffered_send("PONG %s\r\n" % line[1])

            if line[1]=="CAP":
                if line[3]=="LS" and "multi-prefix" in line[3:]:
                    self.buffered_send("CAP REQ multi-prefix\r\n")
                    self.buffered_send("CAP END\r\n")
                    self.buffered_send("NICK %s\r\n" % self.nick)
                    self.buffered_send("USER %s %s bla :%s\r\n" % ("badmutha", "*", "*"))

            # This will later be performed by input
            if line[1]=="376":
                self.join_channel('#humptydumpty')
            
            # This will later be performed by input
            if line[1]=="JOIN":
                self.stack.put((self.privmsg,'Hwhaddup playaaaa'))

        return 1

    def join_channel(self,chan):
        self.channel = chan
        self.buffered_send(''.join(['JOIN ',chan,'\r\n']))

    def privmsg(self, msg):
        self.buffered_send( ''.join(['PRIVMSG ', self.channel, ' :', msg, '\r\n']))

    def topic_change(self, topic):
        self.buffered_send(''.join(['TOPIC', self.channel, topic]))

    def leave_server(self):
        self.buffered_send('QUIT\r\n')

    def leave_channel(self,channel,goodbye=''):
        # TODO: Multiple channel quit (multiple channel everything)
        cmd = ['PART ']
        cmd.append(channel)
        if goodbye != '':
            bye = ''.join([':',goodbye])
            cmd.append(bye)
        cmd.append('\r\n')
        self.buffered_send(''.join(cmd))

    def buffered_send(self,msg):
        if msg:
            sent = self.s.send(msg)
            self.buffered_send(msg[sent:])
        else:
            return

    def __exit__(self, type, value, traceback):
        self.s.close()
        return 0

def main():
    print "huh?"

if __name__=="__main__":
    main()

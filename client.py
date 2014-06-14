#!/usr/bin/python
#
# Basic python client
# Taken from http://www.tutorialspoint.com/python/python_networking.htm
# June 12, 2014

import socket as so

class Connection:
    def __init__(self):
        """
        Stole most of the skeleton of this code from http://oreilly.com/pub/h/1968
        """

        nick = 'BadMuthaUcka'
        port = 6667
        address = 'irc.freenode.net'
        channel = '#python'

        s = so.socket()
        s.connect((address,port))
        s.send("CAP LS\r\n")

        while True:
            readbuffer = ''
            readbuffer = readbuffer+s.recv(1024)
            temp = readbuffer.split("\n")
            readbuffer = temp.pop()

            for line in temp:
                line = line.rstrip()
                line = line.split()
                print line

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

                if line[1]=="470":
                    print 'Kicked!'
                    print line[3:]


    def __exit__(self):
        self.s.close()

def connect(server,user,pwd):
    s = so.socket()
    port = 12345

    s.connect(('', port))
    s.close()

def main():
    print "huh?"

if __name__=="__main__":
    main()

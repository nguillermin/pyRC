#!/usr/bin/env python
#
# Main file. I guess this is where everything will start from

#import getpass

import client

if __name__=="__main__":
    c = client.Connection()
    c.server_connect(('irc.freenode.net',6667))

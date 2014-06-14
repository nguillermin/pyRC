#!/usr/bin/env python
#
# Main file. I guess this is where everything will start from

#import getpass

import client
import time

if __name__=="__main__":
    with client.Connection() as c:
        c.join_server()
        time.sleep(5)
        exit(0)

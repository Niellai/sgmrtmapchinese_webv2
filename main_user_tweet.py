# coding: utf-8
import logging
import socket
import sys
import re
from UserTweetAsync import UserTweet

lock_socket = None 

def is_lock_free():
    global lock_socket
    lock_socket = socket.socket(socket.AF_UNIX, socket.SOCK_DGRAM)
    try:
        # this should be unique. using your username as a prefix is a convention
        lock_id = "niellai.tweetListener"
        lock_socket.bind('\0' + lock_id)
        logging.debug("Acquired lock %r" % (lock_id,))
        return True
    except socket.error:
        # socket already locked, task must already be running
        logging.info("Failed to acquire lock %r" % (lock_id,))
        return False
    
if not is_lock_free():
    sys.exit()
    
userTweet = UserTweet()
userTweet.listen()


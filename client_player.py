#!/usr/bin/env python3
import pickle
import struct
from socket import *

import cv2 as cv

if __name__=="__main__":
    s = socket(AF_INET, SOCK_STREAM)
    s.connect(("", 9090))
    print("connected to server...")

    # save movie in memory
    data = bytearray()

    # size of number used to designate payload size
    # in this case unsigned long long so 8 bytes
    payload_size_size = struct.calcsize("Q")
    
    # read in frames
    print("receiving data from server")
    while len(data) < payload_size_size:
        received = s.recv(4096)

        # connection has been closed
        if len(received) == 0:
            break

        data.extend(received)



    s.close()
    
    print("len of data: {}".format(len(data)))
    # play all at the end for now 
    print("playing back frames")
    i = 0
    while True:
        if i + payload_size_size - 1 > len(data):
            print("got out")
            break

        payload_size = int.from_bytes(
                    data[i:i+payload_size_size], 
                    byteorder="big",
                    signed=False
                )

        i += payload_size_size 
        frame = pickle.loads(bytes(data[i:i+payload_size]))

        i += payload_size

        cv.imshow("frame", frame) 
        if cv.waitKey(40) == ord("q"):
            print("you pressed 'q' and we will exit")
            break

'''
case 1: have incomplete payload_size_size (means I dont' have payload)
case 2: have complete payload_size_size
        case 2.1: have incomplete payload
        case 2.2: have complete payload 
'''


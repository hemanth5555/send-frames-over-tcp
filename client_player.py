#!/usr/bin/env python3
import pickle
import struct
from socket import *
from time import perf_counter as tpf
import cv2 as cv

if __name__=="__main__":
    s = socket(AF_INET, SOCK_STREAM)
    s.connect(("", 9090))
    print("connected to server...")

    # buffer to save frame
    data = bytearray()

    # size of number used to designate payload size
    # in this case unsigned long long so 8 bytes
    payload_size_size = struct.calcsize("Q")
    
    # read in frames
    print("receiving data from server")
    while True:
        # 1 iteration = receiving 1 frame (1 + a little more in some cases)
        start = tpf()

        # first figure out the size of a payload, then build up
        while len(data) < payload_size_size:
            received = s.recv(4096)

            # connection has been closed
            if len(received) == 0:
                break

            data.extend(received)


        # get payload info; which is in the first 8 bytes of the payload
        packed_msg_size = data[:payload_size_size]
        
        # get the message content (everything after the first 8 bytes), which is our frame
        data = data[payload_size_size:]

        # get payload size so we know how much data to read in before we have a full frame
        msg_size = struct.unpack("Q",packed_msg_size)[0]

        # get the actual frame (we know from msg_size how much bytes to recv)
        # might read a little extra bytes, but will handle that 
        while len(data) < msg_size:
            data.extend(s.recv(4096))

        # frame will be data all the way up to msg_size
        frame = data[:msg_size]
        
        # overwrite data, with left over "data" which includes the next frame
        data = data[msg_size:]
        end = tpf()

        # get recv time before displaying image (likely faster than
        # shown on the server side because data has already arrived buffered
        # before calling recv
        print("recv frame time: {:0.3f} seconds".format(end - start))

        #cv.imshow("frame", pickle.loads(frame))
        #if cv.waitKey(40) == ord("q"):
        #    print("you pressed 'q' and we will exit")
        #    break

    s.close()

'''
case 1: have incomplete payload_size_size (means I dont' have payload)
case 2: have complete payload_size_size
        case 2.1: have incomplete payload
        case 2.2: have complete payload 


reading frame by frame adopted from https://stackoverflow.com/questions/49084143/opencv-live-stream-video-over-socket-in-python-3
'''


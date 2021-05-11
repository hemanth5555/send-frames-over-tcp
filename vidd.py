#!/usr/bin/env python3
import sys
import pickle
import struct
import logging as log
from pathlib import Path
from statistics import mean
from time import perf_counter as tpf
from socket import *
import cv2 as cv

def to_mb(b: int) -> float:
    return b / (1 << 20)

if __name__=="__main__":
    VIDEO_FILE = "surf.mp4"
    print("video size: {:0.3f} Mb".format(to_mb(Path(VIDEO_FILE).stat().st_size)))

    s = socket(AF_INET, SOCK_STREAM)
    s.bind(("", 9090))
    s.listen(5)
    s.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    print("listening")

    while True:
        client, addr = s.accept()
        print("connected ...")

        # read video into memory, frame by frame
        cap = cv.VideoCapture(VIDEO_FILE)

        while cap.isOpened():
            ret, frame = cap.read()
        
            # add socket code here
            start = tpf()

            # serialize frame
            frame_p = pickle.dumps(frame)

            # first value in binary string is unsigned long long ('Q') that
            # specifies the length of the following data segment followed
            # by the actual message itself
            payload = struct.pack("Q", len(frame_p)) + frame_p

            # send binary string 

            # will buffer frame and ensure entire payload is sent
            # send() returns # bytes sent, and may send less than payload, so 
            # using sendall isntead
            client.sendall(payload)
            end = tpf()

            print("sent payload of size: {size:0.3f} Mb; {dur:0.3f} seconds".format(
                size=to_mb(sys.getsizeof(payload)),
                dur=end - start
            ))

            if not ret:
                print("Can't receive frame (possibly stream end?).")
                break
        
        client.close()


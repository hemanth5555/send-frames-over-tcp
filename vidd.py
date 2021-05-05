#!/usr/bin/env python3
import sys
import pickle
import struct
from socket import *
import cv2 as cv

if __name__=="__main__":
    # read video into memory, frame by frame
    cap = cv.VideoCapture("surf.mp4")
    frames = list()

    while cap.isOpened():
        ret, frame = cap.read()
        frames.append(frame)

        if not ret:
            print("Can't receive frame (stream end?).")
            break
    
    print("captured {} frames".format(len(frames)))

    s = socket(AF_INET, SOCK_STREAM)
    s.bind(("", 9090))
    s.listen(5)
    s.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    print("listening")

    while True:
        client, addr = s.accept()
        print("connected ...")

        # send frames
        for frame in frames:
            frame_p = pickle.dumps(frame)

            # first value in binary string is unsigned long long ('Q') that
            # specifies the length of the following data segment followed
            # by the actual message itself
            payload = struct.pack("!Q", len(frame_p)) + frame_p

            # send binary string 
            print("sending payload of size: {}".format(sys.getsizeof(payload)))
            client.send(payload)

        client.close()

    

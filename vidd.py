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
from prometheus_client import start_http_server, Counter
from prometheus_client.core import GaugeMetricFamily, REGISTRY, CounterMetricFamily
import logging

def to_mb(b: int) -> float:
    return b / (1 << 20)

if __name__=="__main__":
    # Create and configure logger
    logging.basicConfig(filename="fabric_logger.log",
                    format='%(asctime)s %(message)s',
                    filemode='w')
    # Creating an object
    logger = logging.getLogger()
    # Setting the threshold of logger to DEBUG
    logger.setLevel(logging.DEBUG)

    VIDEO_FILE = "Friends.mp4"
    print("video size: {:0.3f} Mb".format(to_mb(Path(VIDEO_FILE).stat().st_size)))

    s = socket(AF_INET, SOCK_STREAM)
    s.bind(("", 9090))
    s.listen(5)
    s.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    print("listening")
    bytes_sent = Counter('video_bytes_sent', 'Total bytes sent')
    duration = Counter('duration', 'Duration ')

    while True:
        client, addr = s.accept()
        print("connected ...")

        # read video into memory, frame by frame
        cap = cv.VideoCapture(VIDEO_FILE)

        total_payload = 0
        total_time = 0

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
            
            payload_size = CounterMetricFamily("payload_size", "A video payload size", labels=['payload_size'])
            payload_size.add_metric(['payload_size'], to_mb(sys.getsizeof(payload)))
            total_payload = total_payload + to_mb(sys.getsizeof(payload))

            gauge = GaugeMetricFamily("video_duration", "Video duration", labels=["video_duration"])
            gauge.add_metric(['payload_size'], end - start)
            total_time = total_time + end - start

            #bytes_sent.inc(to_mb(sys.getsizeof(payload)))
            print("sent payload of size: {size:0.3f} Mb; {dur:0.3f} seconds".format(
                size=to_mb(sys.getsizeof(payload)),
                dur = end - start
            ))
            logger.info("sent payload of size: {size:0.3f} Mb".format(
                size=to_mb(sys.getsizeof(payload))
            ))
            logger.info("duration of stream: {dur:0.3f} seconds".format(dur=end - start))
            logger.info("throughput of network: {throughput:0.3f} bytespersec".format(throughput = total_payload/total_time))

            if not ret:
                print("Can't receive frame (possibly stream end?).")
                break
        
        client.close()


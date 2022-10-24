import os
import re
from time import sleep

from prometheus_client import start_http_server, Counter

def main():
    start_http_server(9002)
    gather_metrics()

def gather_metrics():
    print("collecting fabric metrics")
    stream_duration = Counter('fabric_stream_duration', 'Total duration')
    bytes_sent = Counter('fabric_http_bytes_sent', 'Total bytes sent')
    for line in follow_log("fabric_logger.log"):
        #match = re.match(regex, line)
        if line.startswith('sent payload of size:'):
            bitesize = line[line.index(':') + 1 : line.index('Mb') - 1]
            bytes_sent.inc(float(bitesize))
        elif line.startswith('duration of stream:'):
            duration = line[line.index(':') + 1 : line.index('seconds') - 1]
            stream_duration.inc(float(duration))
        else:
            print("line did not match")

def follow_log(file):
    with open(file, 'r') as f:
        while True:
            line = f.readline()
            if not line:
                sleep(0.1)
                continue
            yield line

if __name__ == '__main__':
    main()
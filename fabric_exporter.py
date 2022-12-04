import os
import re
from time import sleep

from prometheus_client import start_http_server, Counter, Gauge

def main():
    start_http_server(9002)
    gather_metrics()

def gather_metrics():
    print("collecting fabric metrics")
    stream_duration = Counter('fabric_stream_duration', 'Total duration')
    bytes_sent = Counter('fabric_http_bytes_sent', 'Total bytes sent')
    through_put = Gauge('fabric_throughput', 'Throughput of network')
    x = 1
    for line in follow_log("fabric_logger.log"):
        #match = re.match(regex, line)
        print("line number : " + str(x))
        x = x + 1
        if 'sent payload of size:' in line:
            bitesize = line[line.index('size:') + 5 : line.index('Mb') - 1]       
            bytes_sent.inc(float(bitesize))
            print("byte size : " + str(bitesize))
        elif 'duration of stream:' in line:
            duration = line[line.index('stream:') + 7 : line.index('seconds') - 1]
            stream_duration.inc(float(duration))
            print("duration : " + str(duration))
        elif 'throughput of network:' in line:
            throughput = line[line.index('network:') + 8 : line.index('bytespersec') -1]
            through_put.set(float(throughput))
            print("throughput : " + str(throughput))
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
#!/usr/bin/env python

import requests
import threading
import signal
import sys
import os

UNITS = {
    'messages': 0,
    'bytes': 1
}


def echo_to_file(out_folder, data, entry, units):
    with open('{0}/{1}_{2}'.format(out_folder, entry, units), 'a+') as out_file:
        out_file.write(data[entry][UNITS[units]]

def poller(ip, port, out_folder, timeout):
    t = threading.Timer(timeout, poller, [ip, port, timeout])

    r = requests.get('http://{0}:{1}/{2}'.format(ip, port, 'get_of_counts')
    data = r.json()
    echo_to_file(out_folder, data, 'OF_out_counts', 'messages')
    echo_to_file(out_folder, data, 'OF_out_counts', 'bytes')

    echo_to_file(out_folder, data, 'OF_in_counts', 'messages')
    echo_to_file(out_folder, data, 'OF_in_counts', 'bytes')

    r = requests.get('http://{0}:{1}/{2}'.format(ip, port, 'get_of13_counts')
    data = r.json()
    echo_to_file(out_folder, data, 'OF13_OFPT_ECHO_REPLY', 'messages')
    echo_to_file(out_folder, data, 'OF13_OFPT_ECHO_REPLY', 'bytes')

    echo_to_file(out_folder, data, 'OF13_OFPT_ECHO_REQUEST', 'messages')
    echo_to_file(out_folder, data, 'OF13_OFPT_ECHO_REQUEST', 'bytes')

    echo_to_file(out_folder, data, 'OF13_OFPT_FLOW_MOD', 'messages')
    echo_to_file(out_folder, data, 'OF13_OFPT_FLOW_MOD', 'bytes')

    echo_to_file(out_folder, data, 'OF13_OFPT_MULTIPART_REPLY', 'messages')
    echo_to_file(out_folder, data, 'OF13_OFPT_MULTIPART_REPLY', 'bytes')

    echo_to_file(out_folder, data, 'OF13_OFPT_MULTIPART_REQUEST', 'messages')
    echo_to_file(out_folder, data, 'OF13_OFPT_MULTIPART_REQUEST', 'bytes')

    echo_to_file(out_folder, data, 'OF13_OFPT_PACKET_IN', 'messages')
    echo_to_file(out_folder, data, 'OF13_OFPT_PACKET_IN', 'bytes')

    echo_to_file(out_folder, data, 'OF13_OFPT_PACKET_OUT', 'messages')
    echo_to_file(out_folder, data, 'OF13_OFPT_PACKET_OUT', 'bytes')

    return t


def post_process(out_folder):
    for cnt_file in os.listdir(out_folder):
        counts = []
        bandwidth = []
        with open('{0}/{1}'.format(out_folder, cnt_file)) as cnt_fd:
            counts = [int(line.rstrip('\n')) for line in cnt_fd]
        bandwidth = [y - x for x,y in zip(counts, counts[1:])]
        with open('{0}/bandwidth_{1}'.format(out_folder, cnt_file), 'a+') as band_fd:
            for el in bandwidth:
                band_fd.write(el)

def main(args):

    poll_t = poller(args.rest_host, args.rest_port, args.out_folder, args.timeout)
    def catch_ctrlc(sig, frame):
        print "You pressed CTRL-C. Exiting..."
        poll_t.cancel()
        post_process(args.out_folder)
        sys.exit()

    signal.signal(signal.SIGINT, catch_ctrlc)



if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--rest-host',
                        required=True,
                        type=str,
                        dest='rest_host',
                        action='store',
                        help='IP address or hostname of the interface the REST'
                             ' server should listen to')
    parser.add_argument('--rest-port',
                        required=True,
                        type=str,
                        dest='rest_port',
                        action='store',
                        help='Port number the REST server should listen to')
    parser.add_argument('--timeout',
                        required=True,
                        dest='out_folder',
                        action='store',
                        default='/tmp/.of_bandwidth_counts',
                        help='Interval between samples in seconds')
    parser.add_argument('--out-folder',
                        required=False,
                        dest='out_folder',
                        action='store',
                        default='/tmp/.of_bandwidth_counts',
                        help='The folder where we will store the bandwidth counts')

    args = parser.parse_args()

    if not os.path.exists(args.out_folder):
        os.makedirs(args.out_folder)

    main(args)
    

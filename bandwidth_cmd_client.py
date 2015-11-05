#!/usr/bin/env python

import argparse
import requests
import time
import signal
import sys
import os

UNITS = {
    'messages': 0,
    'bytes': 1
}

of13_types = [
    'OFPT_HELLO',
    'OFPT_ERROR',
    'OFPT_ECHO_REQUEST',
    'OFPT_ECHO_REPLY',
    'OFPT_EXPERIMENTER',
    'OFPT_FEATURES_REQUEST',
    'OFPT_FEATURES_REPLY',
    'OFPT_GET_CONFIG_REQUEST',
    'OFPT_GET_CONFIG_REPLY',
    'OFPT_SET_CONFIG',
    'OFPT_PACKET_IN',
    'OFPT_FLOW_REMOVED',
    'OFPT_PORT_STATUS',
    'OFPT_PACKET_OUT',
    'OFPT_FLOW_MOD',
    'OFPT_GROUP_MOD',
    'OFPT_PORT_MOD',
    'OFPT_TABLE_MOD',
    'OFPT_MULTIPART_REQUEST',
    'OFPT_MULTIPART_REPLY',
    'OFPT_BARRIER_REQUEST',
    'OFPT_BARRIER_REPLY',
    'OFPT_QUEUE_GET_CONFIG_REQUEST',
    'OFPT_QUEUE_GET_CONFIG_REPLY',
    'OFPT_ROLE_REQUEST',
    'OFPT_ROLE_REPLY',
    'OFPT_GET_ASYNC_REQUEST',
    'OFPT_GET_ASYNC_REPLY',
    'OFPT_SET_ASYNC',
    'OFPT_METER_MOD'
]


def echo_of_counts(out_folder, data, entry, units, prepend_fname=None):
    if entry not in data.keys():
        return
    filename = '{0}_{1}'.format(entry, units)
    if prepend_fname is not None:
        filename = '{0}_{1}'.format(prepend_fname, filename)
    with open('{0}/{1}'.format(out_folder, filename), 'a+') as out_file:
        out_file.write(str(data[entry][UNITS[units]]))
        out_file.write('\n')

def echo_of13_counts(out_folder, data, in_or_out):
    if in_or_out not in data.keys():
        return
    for of_msg_type in of13_types:
        echo_of_counts(out_folder, data[in_or_out], of_msg_type, 'messages', prepend_fname=in_or_out)
        echo_of_counts(out_folder, data[in_or_out], of_msg_type, 'bytes', prepend_fname=in_or_out)


def poller(ip, port, out_folder):
    r = requests.get('http://{0}:{1}/{2}'.format(ip, port, 'get_of_counts'))
    data = r.json()
    echo_of_counts(out_folder, data, 'OF_out_counts', 'messages')
    echo_of_counts(out_folder, data, 'OF_out_counts', 'bytes')

    echo_of_counts(out_folder, data, 'OF_in_counts', 'messages')
    echo_of_counts(out_folder, data, 'OF_in_counts', 'bytes')

    r = requests.get('http://{0}:{1}/{2}'.format(ip, port, 'get_of13_counts'))
    data = r.json()
    
    echo_of13_counts(out_folder, data, 'OF13_in_counts')
    echo_of13_counts(out_folder, data, 'OF13_out_counts')


def post_process(out_folder):
    for cnt_file in os.listdir(out_folder):
        counts = []
        bandwidth = []
        with open('{0}/{1}'.format(out_folder, cnt_file)) as cnt_fd:
            counts = [int(line.rstrip('\n')) for line in cnt_fd]
        bandwidth = [y - x for x,y in zip(counts, counts[1:])]
        with open('{0}/bandwidth_{1}'.format(out_folder, cnt_file), 'a+') as band_fd:
            for el in bandwidth:
                band_fd.write(str(el))
                band_fd.write('\n')

def main(args):
    def catch_ctrlc(sig, frame):
        print "You pressed CTRL-C. Exiting..."
        post_process(args.out_folder)
        sys.exit()

    signal.signal(signal.SIGINT, catch_ctrlc)
    while True:
        poller(args.rest_host, args.rest_port, args.out_folder)
        time.sleep(float(args.timeout))


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
                        dest='timeout',
                        action='store',
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
    

# oftraf

RESTful OpenFlow traffic monitor

Filters OpenFlow packets from a network interface and reports statistics. 

Features:

- **Summary and detailed OF statistics in real-time**: summary statistics refer to 
  total incoming and outgoing OF traffic (from the viewpoint of the SDN 
  controller). Detailed statistics offer a finer-grain breakdown based on the OF 
  message type. Both classes are being updated and displayed in real-time.
- Support for **OF1.0 and OF1.3 protocols**
- **REST interface** for accessing statistics. This enables remote online 
  monitoring of a controller's incoming and outgoing OF traffic.

# Requirements

- Python 2
- `pypcap`, `dpkt` and `bottle` Python packages

On an Ubuntu-based machine, install the required packages as follows: 

```bash
sudo apt-get install python-pypcap python-dpkt python-bottle
```

# Usage

```bash
sudo python oftraf.py --rest-host <host> --rest-port <port> --of-port <ofport> --ifname <interface> [--server]
```

Command line arguments: 

- `--rest-host`: the IP or hostname of the interface the REST server should listen to
- `--rest-port`: the port the REST server should listen to
- `--of-port`: the OpenFlow port number based on which packet filtering will take place
- `--ifname`: the network interface to sniff packets from
- `--server`: run `oftraf` as server only without printing stats

Example: 

1. Launch an SDN controller and a Mininet topology on the same machine
2. Launch `oftraf`:  
  ```bash
  sudo python oftraf.py --rest-host localhost --rest-port 5555 --of-port 6653 --ifname lo
  ```
  This starts sniffing and counting OF packets on the `lo` interface. The statistics are 
  being displayed in real-time in a curses-based console which refreshes every 1 second.
  Sample output: 
  
  ```
  Elapsed seconds:994.4902
  OF in pps:             29390.0
  OF in Bps:           3885368.0
  OF out pps:            31300.0
  OF out Bps:          3964004.0

  Packet Type                           Count          Bytes
  --------------------------------------------------------------
  Total OF in:                          700581         212923343
  Total OF out:                         366417         114676077
  OF13_OFPT_ECHO_REPLY:                 3088           185528
  OF13_OFPT_ECHO_REQUEST:               3092           185520
  OF13_OFPT_FLOW_MOD:                   353            81460
  OF13_OFPT_MULTIPART_REPLY:            445024         171816903
  OF13_OFPT_MULTIPART_REQUEST:          40668          87600195
  OF13_OFPT_PACKET_IN:                  245614         40563432
  OF13_OFPT_PACKET_OUT:                 9469           10533154
  ```
  
  **OF in** and **OF out** refer to OF traffic traveling into and out of the SDN controller,
  respectively. **pps** and **Bps** are packets-per-second and bytes-per-second.
  
3. The REST server starts together with `oftraf`. Let's try to send some statistics requests. 

  On another console, issue the following REST request to access summary statistics: 
  ```bash
  curl  http://localhost:5555/get_of_counts
  ```
  Response: 

  ```json
  {
    "OF_out_counts": [366417, 114676077], 
    "OF_in_counts": [700581, 212923343]
  }
  ```
  In each statistic returned, the first number (e.g. 366417) is the packet count, and the 
  second (114676077) is the byte count. 
  
  `OF_out_counts` refers to the packets travelling from the controller to the 
  switches, `OF_in_counts` refers to the packets travelling at the opposite 
  direction. 
  
  To access detailed OF13 statistics, issue the following REST request:

  ```bash
  curl http://localhost:5555/get_of13_counts
  ```

  Response: 

  ```json
  {
    "OF13_OFPT_ECHO_REPLY": [3088, 185528],
    "OF13_OFPT_ECHO_REQUEST": [3092, 185520],
    "OF13_OFPT_FLOW_MOD": [353, 81460],
    "OF13_OFPT_MULTIPART_REPLY": [445024, 171816903],
    "OF13_OFPT_MULTIPART_REQUEST": [40668, 87600195],
    "OF13_OFPT_PACKET_IN": [245614, 40563432],
    "OF13_OFPT_PACKET_OUT": [9469, 10533154]
  }
  ```
  
  Similarly, use the following REST request for OF10 statistics: 
  
  ```bash
  curl http://localhost:5555/get_of10_counts
  ```

4. To stop `oftraf`, hit Ctrl-C in the console where it runs, or issue a 
   REST request as follows: 

   ```bash
   $ curl  http://localhost:5555/stop
   ```


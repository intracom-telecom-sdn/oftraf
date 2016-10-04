#!/bin/bash

# Copyright (c) 2015 Intracom S.A. Telecom Solutions. All rights reserved.
# -----------------------------------------------------------------------------
# This program and the accompanying materials are made available under the
# terms of the Eclipse Public License v1.0 which accompanies this distribution,
# and is available at http://www.eclipse.org/legal/epl-v10.html

# $1 virtual env base path
# $2 PYTHONPATH
# $3 Handler path for OFTRAF
# $4 --rest-host: the IP or hostname of the interface the REST server should listen to
# $5 --rest-port: the port the REST server should listen to
# $6 --of-port: the OpenFlow port number based on which packet filtering will take place
# $7 --ifname: the network interface to sniff packets from
# $8 --server: run oftraf as server only without printing stats

if [ "$#" -eq 4 ]
then
    source $1/bin/activate; PYTHONPATH=$2 python $3 --rest-host $4 --rest-port $5 --of-port $6 --of-port $7 --server
else
    echo "Invalid number of arguments."
    exit 1
fi
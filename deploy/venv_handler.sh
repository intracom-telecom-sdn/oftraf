#!/bin/bash

# Copyright (c) 2015 Intracom S.A. Telecom Solutions. All rights reserved.
# -----------------------------------------------------------------------------
# This program and the accompanying materials are made available under the
# terms of the Eclipse Public License v1.0 which accompanies this distribution,
# and is available at http://www.eclipse.org/legal/epl-v10.html

# $1 virtual env base path
# $2 Handler path for OFTRAF
# $3 --rest-host: the IP or hostname of the interface the REST server should listen to
# $4 --rest-port: the port the REST server should listen to
# $5 --of-port: the OpenFlow port number based on which packet filtering will take place
# $6 --ifname: the network interface to sniff packets from
#    --server: run oftraf as server only without printing stats

if [ "$#" -eq 6 ]
then
    source $1/bin/activate; python $2 --rest-host $3 --rest-port $4 --of-port $5 --of-port $6 --server &
elif [ "$#" -eq 5 ]
then
    python $1 --rest-host $2 --rest-port $3 --of-port $4 --of-port $5 --server
else
    echo "Invalid number of arguments."
    exit 1
fi
#!/bin/bash

# Copyright (c) 2015 Intracom S.A. Telecom Solutions. All rights reserved.
#
# This program and the accompanying materials are made available under the
# terms of the Eclipse Public License v1.0 which accompanies this distribution,
# and is available at http://www.eclipse.org/legal/epl-v10.html

$HOME/mininet/bin/mn &
sleep 30
curl http://localhost:5555/get_of10_counts
echo
curl http://localhost:5555/get_of_counts
echo

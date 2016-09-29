#!/bin/bash

# Copyright (c) 2015 Intracom S.A. Telecom Solutions. All rights reserved.
#
# This program and the accompanying materials are made available under the
# terms of the Eclipse Public License v1.0 which accompanies this distribution,
# and is available at http://www.eclipse.org/legal/epl-v10.html

BASE_DIR="/opt"
VENV_DIR="venv_oftraf"

# OFTRAF provisioning actions
#------------------------------------------------------------------------------
mkdir $BASE_DIR/$VENV_DIR

apt-get update && apt-get install -y \
    python \
    python3.4 \
    python-dev \
    python3.4-dev \
    python-virtualenv

wget https://raw.githubusercontent.com/intracom-telecom-sdn/oftraf/master/requirements.txt -P $BASE_DIR
source $BASE_DIR/$VENV_DIR/bin/activate
pip3 $pip_options install -r $BASE_DIR/requirements.txt
rm -rf $BASE_DIR/requirements.txt
deactivate
#apt-get -y update
#apt-get install -y git python python-pypcap python-dpkt python-bottle
#git clone http://github.com/mininet/mininet $HOME/mininet
#cd $HOME/mininet && git checkout -b 2.2.1
#$HOME/mininet/util/install.sh -n3fv

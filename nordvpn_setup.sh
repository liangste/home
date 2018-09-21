#!/bin/bash

sudo apt-get update && sudo apt-get -y upgrade
sudo apt-get -y install openvpn ca-certificates unzip python-pip
pip install pyping

cd /etc/openvpn

sudo wget https://downloads.nordcdn.com/configs/archives/servers/ovpn.zip
sudo unzip ovpn.zip
sudo rm *.zip

cd ovpn_tcp

CREDENTIALFILE=/etc/openvpn/credentials
sudo sed -i -e 's|auth-user-pass|auth-user-pass /etc/openvpn/credentials|g' ca*.ovpn
sudo touch $CREDENTIALFILE

echo "save your credentials username'\n'password in $CREDENTIALFILE"
echo "update your physical location in nordvpn_connect.py::home_location"

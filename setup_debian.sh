#!/usr/bin/env bash

sudo apt-get install libavahi-compat-libdnssd-dev git make -y
curl -sL https://deb.nodesource.com/setup_7.x | sudo -E bash -
sudo apt-get install -y nodejs
sudo npm install -g --unsafe-perm mdns
sudo npm install -g --unsafe-perm homebridge
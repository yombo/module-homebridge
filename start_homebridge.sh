#!/bin/bash
CONFIG=$1
PLUGIN=$2
homebridge -D -U $1 -P $2

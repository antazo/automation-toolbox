#!/bin/bash

__author__ = "Alex Antazo"


# Receives the process names as arguments (eg. "ffmpeg Xorg"),
# returns all the process IDs that have those names and 
# give them priority 19.

for pid in $(pidof $@); do renice 19 $pid; done


# Receives the process names as arguments (eg. "ffmpeg Xorg"),
# returns all the process IDs that have those names and 
# send them the CONT signal, and wait 1 second until the process is done for the next check.

# for pid in $(pidof $@); do while kill -CONT $pid; do sleep 1; done; done
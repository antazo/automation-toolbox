#!/usr/bin/env python3

import psutil

# check CPU usage
psutil.cpu_percent()

# check disk I/O
psutil.disk_io_counters()

# check the network I/O bandwidth
psutil.net_io_counters()

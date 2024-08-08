#!/usr/bin/env python3

import logging
# try structlog or colorlog

# Set the minimum logging level to INFO,
logging.basicConfig(level=logging.INFO)

# Get a logger object
log = logging.getLogger(__name__)

# Start the log file
log.info("Hello world")

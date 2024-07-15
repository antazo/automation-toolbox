#!/usr/bin/env python3
"""
Using Python threads with the "ThreadPoolExecutor"
from the "futures" module, to be able to run things
in parallel.

It's like using "daemonize -c" in Bash.

This is the function with expensive operations
for this example:
    process_file(root, basename)
"""

from concurrent import futures

def main():
    executor = futures.ThreadPoolExecutor()
    #executor = futures.ProcessPoolExecutor()

    # Now we would pass the function to the executor,
    # to distribute among the different workers:

    #executor.submit(process_file=, root, basename)

    print("Waiting for all threads to finish.")
    executor.shutdown()
    return 0


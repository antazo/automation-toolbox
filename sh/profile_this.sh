#!/bin/bash

__author__ = "Alex Antazo"


# Receives the command we are profiling as arguments (eg. "./send_reminder.py"),
# generates a file with the profiler output in a specific format

pprofile3 -f callgrid -o profile.out $@


# Opens the generated output in a profile visualizer

# kcachegrind profile.out
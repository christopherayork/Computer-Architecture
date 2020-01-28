#!/usr/bin/env python3

"""Main."""

import sys
from cpu import *

filename = './examples/print8.ls8'
if len(sys.argv) > 1: filename = sys.argv[1]
cpu = CPU()

if filename is not None:
    cpu.load(filename)
    cpu.run()
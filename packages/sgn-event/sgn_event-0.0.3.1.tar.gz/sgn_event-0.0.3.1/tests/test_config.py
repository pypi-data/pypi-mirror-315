#!/usr/bin/env python3

import sys

import numpy
import yaml

from sgnevent.base import EventBuffer, dtype_from_config


def test_config(config):
    dtype = {
        n: dtype_from_config(config[n])
        for n in ("filter", "simulation", "data", "trigger", "event")
    }
    print(dtype)

    event_dict = {
        n: EventBuffer(0, 1_000_000_000, data=numpy.zeros(3, d))
        for (n, d) in dtype.items()
    }
    print(event_dict)


with open(sys.argv[1]) as f:
    config = yaml.safe_load(f)

test_config(config)

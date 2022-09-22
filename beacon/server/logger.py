#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import logging

def load_logger():
    logger = logging.getLogger('simple_example')
    logger.setLevel(logging.DEBUG)
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    ch.setFormatter(formatter)
    logger.addHandler(ch)
    return logger

LOG = load_logger()
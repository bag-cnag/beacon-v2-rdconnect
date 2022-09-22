#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import yaml
import pathlib
import logging
import warnings

from logging.config import dictConfig

logging.captureWarnings(True)
warnings.simplefilter('default')

def load_logger():
    log_file =  pathlib.Path(__file__).parent / 'logger.yml'
    with open(log_file, 'r') as stream:
        dictConfig(yaml.safe_load(stream))
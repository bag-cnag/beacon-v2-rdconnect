#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Beacon API Web Server for RD-Connect (R) at CNAG-CRG.
Designed with async/await programming model.

Author: Carles Hernandez-Ferrer
Date: May 3th, 2021

Server implements the following endpoints from API:
 * ...

Logging model was obtained from refrence implementation of Beacon 2.x by EGA/CRG.
JSON viewer was obtained from: https://www.jqueryscript.net/other/jQuery-Plugin-For-Easily-Readable-JSON-Data-Viewer.html
"""

__title__ = 'Beacon v2.0.0.d3'
__version__ = VERSION = '2.0.0.d3'
__author__ = 'CNAG-CRG Bioinformatic Unit, Analysis Team'
__license__ = 'MIT'
__copyright__ = 'Beacon 2.0.0.d5 @ CNAG-CRG, Barcelona, Spain'

import os
import base64
import logging

from aiohttp import web
from pathlib import Path
from time import strftime

from server.config import config
from server.endpoints import routes
from server.logger import load_logger

LOG = logging.getLogger(__name__)

def main():
    """Run the beacon API."""

    # Configure logging system
    # load_logger() # TODO
    logging.basicConfig(level=logging.DEBUG)
    
    # Create beacon
    beacon = web.Application()

    # Add API' endpoints
    beacon.add_routes(routes)
    LOG.debug(routes)

    # Start web server
    web.run_app(beacon,
        host = getattr(config, 'beacon_host', '0.0.0.0'),
        port = getattr(config, 'beacon_port',      5050),
        shutdown_timeout = 0, ssl_context = None
    )

if __name__ == '__main__':
    main()

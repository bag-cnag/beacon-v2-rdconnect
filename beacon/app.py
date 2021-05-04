#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Beacon API Web Server for RD-Connect (R) at CNAG-CRG.
Designed with async/await programming model.

Author: Carles Hernandez-Ferrer
Date: May 3th, 2021

Server implements the following endpoints from API:
 * ...

Logging model was ibtained from refrence implementation of Beacon 2.x by EGA/CRG.
JSON viewer was obtained from: https://www.jqueryscript.net/other/jQuery-Plugin-For-Easily-Readable-JSON-Data-Viewer.html
"""

__title__ = 'Beacon v2.0.0.d3'
__version__ = VERSION = '2.0.0.d3'
__author__ = 'CNAG-CRG Bioinformatic Unit, Analysis Team'
__license__ = 'MIT'
__copyright__ = 'Beacon 2.0.0.d5 @ CNAG-CRG, Barcelona, Spain'


import os
import base64
import jinja2
import logging
import aiohttp_jinja2

from aiohttp import web
from pathlib import Path
from time import strftime

# from . import conf, load_logger, endpoints
# from .utils import db, middlewares

from server.config import config
from server.utils import streamer, middleware
from server.endpoints import routes
from server.logger import load_logger

LOG = logging.getLogger(__name__)

async def initialize(app):
    app['static_root_url'] = '/static'
    env = aiohttp_jinja2.get_env(app)
    env.globals.update(
        #len=len,
        #max=max,
        #enumerate=enumerate,
        #range=range,
        config = config,
        #now=strftime("%Y")
    )
    LOG.info("Initialization done.")

# async def destroy(app):
#     LOG.info("Shutting down.")

def main():
    """Run the beacon API."""

    # Configure logging system
    #load_logger()
    logging.basicConfig(level=logging.DEBUG)
    
    # Create beacon
    beacon = web.Application()
    beacon.on_startup.append(initialize)
    LOG.info("Initialization done.")

    # Prepare a basic UI
    main_dir = Path(__file__).parent.resolve()
    # Templates locations
    template_loader = jinja2.FileSystemLoader(str(main_dir / 'ui' / 'templates'))
    aiohttp_jinja2.setup(beacon, loader = template_loader)

    # Attach middleware (secion + csrf)
    middleware.setup(beacon)

    # Add API' endpoints
    beacon.add_routes(routes)

    # # Configure HTTPS (or not)
    # ssl_context = None
    # if getattr(conf, 'beacon_tls_enabled', False):
    #     use_as_client = getattr(conf, 'beacon_tls_client', False)
    #     sslcontext = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH if use_as_client else ssl.Purpose.SERVER_AUTH)
    #     sslcontext.load_cert_chain(conf.beacon_cert, conf.beacon_key) # should exist
    #     sslcontext.check_hostname = False
    #     # TODO: add the CA chain

    static_files = Path(__file__).parent.resolve() / 'ui' / 'static'
    beacon.add_routes([web.static('/static', str(static_files), show_index=True)])
    web.run_app(beacon,
        host=getattr(config, 'beacon_host', '0.0.0.0'),
        port=getattr(config, 'beacon_port', 5050),
        shutdown_timeout=0#, ssl_context=ssl_context
    )


if __name__ == '__main__':
    main()

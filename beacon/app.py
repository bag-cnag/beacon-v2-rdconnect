#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Beacon API Web Server for RD-Connect (R) at CNAG-CRG.
Designed with async/await programming model.

Author: Carles Hernandez-Ferrer
Last update: November, 24th, 2021
Creation date: May 3th, 2021

"""

__title__ = 'Beacon v2.0.0.d4'
__version__ = VERSION = '2.0.0.d4'
__author__ = 'CNAG-CRG Bioinformatic Unit, Analysis Team'
__license__ = 'MIT'
__copyright__ = 'Beacon 2.0.0.d4 @ CNAG-CRG, Barcelona, Spain'


from aiohttp import web
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

from server.config import config
from server.logger import LOG
from server.framework.endpoints import routes

def main():
    config.load_filts()

    beacon = web.Application()
    beacon.add_routes(routes)
    web.run_app(beacon,
        host = getattr(config, 'beacon_host', '0.0.0.0'),
        port = getattr(config, 'beacon_port',      5050),
        shutdown_timeout = 0, 
        ssl_context = None
    )

if __name__ == '__main__':
    main()

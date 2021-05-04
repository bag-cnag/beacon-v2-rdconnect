#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import logging

from aiohttp import web
from aiohttp.http import SERVER_SOFTWARE

from ..config import config

LOG = logging.getLogger(__name__)

async def json_reponse(request, data):
    LOG.debug('HTTP response')
    headers = {
        'Server': f'{config.beacon_name} {config.api_version} (based on {SERVER_SOFTWARE})'
    }
    return web.json_response(data, status = 200, headers = headers, content_type = 'application/json')

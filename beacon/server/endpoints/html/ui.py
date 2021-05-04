#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import logging

from aiohttp_jinja2 import template
from aiohttp_csrf import generate_token
from aiohttp_session import get_session

#from ...utils import db, resolve_token, middlewares
import json
from server.config import config

LOG = logging.getLogger(__name__)

@template('index.html')
async def index(request):
    csrf_token = await generate_token(request)

    session = await get_session(request)
    access_token = session.get('access_token')
    #datasets, authenticated = await resolve_token(access_token, [])
    #LOG.debug('Datasets: %s', datasets)
    return {
        'request': request,
        'session': session,
        #'assemblyIDs': await db.fetch_assemblyids(),
        #'datasets': datasets, #db.fetch_datasets_access(datasets=datasets),
        'form': {},
        #'selected_datasets': set(),
        #'filters': set(),
        'beacon_response': json.dumps({'response': 'loggin to start using the demo endpoints for Beacon v2 API'}),
        'cookies': request.cookies,
        'csrf_token': f'<input type="hidden" name="{config.crsf_field_name}" value="{csrf_token}" />',
    }
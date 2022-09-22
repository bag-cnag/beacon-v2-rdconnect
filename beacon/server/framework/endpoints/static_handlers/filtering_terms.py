#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from server.config import config
from server.logger import LOG
from server.framework.utils import json_response

# def filtering_terms(request):    
def filtering_terms():
    async def wrapper( request ):
        rsp = {
            'meta': {
                'beaconId':	config.beacon_id,
                'apiVersion': config.api_version,
                'responseType': 'filteringTerm',
                'returnedSchemas': [ {
                    'entityType': 'filteringTerm',
                    'schema': 'https://raw.githubusercontent.com/ga4gh-beacon/beacon-framework-v2/main/definitions/FilteringTerm'
                } ],
            },
            'response': {
                'filteringTerms': config.filters_out
            }
        }
        return await json_response( request, rsp )
    return wrapper


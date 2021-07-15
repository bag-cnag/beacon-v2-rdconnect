#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import logging

from server.validation.fields import ChoiceField, RegexField, SchemaField
from server.validation.request import RequestParameters
from server.utils.streamer import json_response
from server.endpoints.response.info_schema import build_beacon_response, build_service_info_response, ga4gh_service_info_v10


LOG = logging.getLogger(__name__)

class InfoParameters(RequestParameters):
    model = ChoiceField('ga4gh-service-info-v1.0', default=None)
    requestedSchema = SchemaField('ga4gh-service-info-v1.0',
                                  'beacon-info-v2.0.0-draft.4',
                                  default='beacon-info-v2.0.0-draft.4')
    apiVersion = RegexField(r'^v[0-9]+(\.[0-9]+)*$')

proxy_info = InfoParameters()

def info(entity):
    async def wrapper(request):
        print("hello")
        LOG.info('Running a GET info request')
        _, qparams_db = await proxy_info.fetch(request)

        response_converted = build_beacon_response([], qparams_db, build_service_info_response, [])

        return await json_response(request, response_converted)
    return wrapper


def ga4gh(request):
    async def wrapper(request):
        LOG.info('Running a GET service-info request')
        return await json_response(request, ga4gh_service_info_v10(None))
    return wrapper

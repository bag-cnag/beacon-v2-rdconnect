#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Custom API exception reponses.
API specification requires custom messages upon error.
"""

import json
import logging

from aiohttp import web

from server.config import config

LOG = logging.getLogger(__name__)

def make_response(error_code, error, fields = None):
    """Return request data as dictionary."""
    LOG.error('Error %s: %s', error_code, error)
    
    return {
        'meta': {
            'beaconId': config.beacon_id,
            'apiVersion': config.api_version,
            'receivedRequest': {
                'meta': {
                    'requestedSchema': dict(fields or []),
                },
                'query': None,
            },
            'returnedSchemas': [],
            'returnedGranularity': "count",
            'receivedRequestSummary':  {
                'apiVersion': 'v2.0',
                'requestedSchemas': [],         
                'requestedGranularity': 'count',
                'pagination': {
                    'skip': 1,
                    'limit': 5,
                }
            }
        },
        'response': {
            'exists': False,
            'error': {'errorCode': error_code,
                      'errorMessage': error},
        },
        'responseSummary': {'exists': False},
        
    }

class BeaconBadRequest(web.HTTPBadRequest):
    """Exception returns with 400 code and a custom error message.

    The method is called if one of the required parameters are missing or invalid.
    Used in conjuction with JSON Schema validator.
    """
    api_error = True
    def __init__(self, error, fields = None, api_error = True):
        """Return custom bad request exception."""
        self.api_error = api_error
        if api_error:
            content = json.dumps(make_response(400, error, fields = fields))
            headers = { 'Content-Type': 'application/json' }
        else:
            content = error
            headers = None
        super().__init__(text = content, headers = headers)

class BeaconUnauthorised(web.HTTPUnauthorized):
    """HTTP Exception returns with 401 code with a custom error message.

    The method is called if the user is not registered or if the token from the authentication has expired.
    Used in conjuction with Token authentication aiohttp middleware.
    """
    api_error = True
    def __init__(self, error, fields = None, api_error = True):
        """Return custom unauthorized exception."""
        self.api_error = api_error
        # we use auth scheme Bearer by default
        if api_error:
            content = json.dumps(make_response(401, error, fields = fields))
            headers = { 'Content-Type': 'application/json' }
        else:
            content = error
            headers = None
        super().__init__(text=content, headers=headers)


class BeaconForbidden(web.HTTPForbidden):
    """HTTP Exception returns with 403 code with the error message.

    If user not autenticated, this is the default outcome from each endpoints.
    """
    api_error = True
    def __init__(self, error, fields = None, api_error = True):
        """Return custom forbidden exception."""
        self.api_error = api_error
        if api_error:
            content = json.dumps(make_response(403, error, fields = fields))
            headers = { 'Content-Type': 'application/json' }
        else:
            content = error
            headers = None
        super().__init__(text = content, headers = headers)


class BeaconServerError(web.HTTPInternalServerError):
    """HTTP Exception returns with 500 code with the error message.

    The 500 error is not specified by the Beacon API, thus as simple error would do.
    """
    api_error = True
    def __init__(self, error, fields = None, api_error = True):
        """Return custom forbidden exception."""
        self.api_error = api_error
        if api_error:
            content = json.dumps(make_response(500, error, fields = fields))
            headers = { 'Content-Type': 'application/json' }
        else:
            content = error
            headers = None
        super().__init__(text=content, headers=headers)


class BeaconEndPointNotImplemented(web.HTTPInternalServerError):
    """HTTP Exception returns with 501 code with the error message.

    The 501 error is not specified by the Beacon API, thus as simple error would do.
    """
    api_error = True
    def __init__(self, error = 'This endpoit is not implemented', fields = None, api_error = True):
        """Return custom forbidden exception."""
        self.api_error = api_error
        if api_error:
            content = json.dumps(make_response(501, error, fields = fields))
            headers = { 'Content-Type': 'application/json' }
        else:
            content = error
            headers = None
        super().__init__(text = content, headers = headers)

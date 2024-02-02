#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from server.config import config
from server.logger import LOG
from server.framework.utils import json_response


#def info( request ):
def info():
    async def wrapper( request ):
        LOG.debug( 'Running a GET "ga4gh" request' )
        return await json_response( request, beacon_info() )
    return wrapper

def beacon_info():
    return {
        'meta': {
            'beaconId': config.beacon_id,
            'apiVersion': config.api_version,
            'returnedSchemas': [ {
                'entityType': 'map',
                'schema': 'https://raw.githubusercontent.com/ga4gh-beacon/beacon-framework-v2/main/responses/beaconInfoResponse.json',
            } ],
        },
        'response': {
            'id': config.beacon_id,
            'name': config.beacon_name,
            'apiVersion': config.api_version,
            'environment': config.environment,
            'organization': {
                'id': config.org_id,
                'name': config.org_name,
                'description': config.org_description,
                'address': config.org_address,
                'welcomeUrl': config.org_welcome_url,
                'contactUrl': config.org_contact_url,
                'logoUrl': config.org_logo_url,
                #'info': config.org_info,
            },
            'description': config.description,
            'version': config.version,
            'welcomeUrl': config.welcome_url,
            'alternativeUrl': config.alternative_url,
            'createDateTime': config.create_datetime,
            'updateDateTime': config.update_datetime,
            'serviceType': config.service_type,
            'serviceUrl': config.service_url,
            'entryPoint': config.entry_point,
            'open': config.is_open,
            #'info': None,
        }
    }
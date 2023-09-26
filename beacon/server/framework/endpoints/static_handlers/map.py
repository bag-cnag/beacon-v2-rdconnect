#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from server.config import config
from server.logger import LOG
from server.framework.utils import json_response


#def map( request ):
def map():
    async def wrapper( request ):
        LOG.debug( 'Running a GET "map" request' )
        rsp = {
            'meta': {
                'beaconId': config.beacon_id,
                'apiVersion': config.api_version,
                'returnedSchemas': [ {
                    'entityType': 'map',
                    'schema': 'https://raw.githubusercontent.com/ga4gh-beacon/beacon-framework-v2/main/responses/beaconMapResponse.json',
                } ],
            },
            'response': {
                '$schema': 'https://raw.githubusercontent.com/ga4gh-beacon/beacon-framework-v2/main/responses/beaconMapResponse.json',
                'title': 'Beacon Map',
                'description': 'Map of a Beacon, its entry types and endpoints. It is conceptually similar to a website sitemap.',
                'endpointSets': {
                    'dataset': {
                        'entryType': 'dataset',
                        'rootUrl': '{}api/datasets'.format( config.server_api_url ),
                        'singleEntryUrl': '{}api/datasets/"id"'.format( config.server_api_url ),
                        'endpoints': {}
                    },
                    'biosample': {
                        'entryType': 'biosample',
                        'rootUrl': '{}api/biosamples'.format( config.server_api_url ),
                        'singleEntryUrl': '{}api/biosamples/"id"'.format( config.server_api_url ),
                        'endpoints': {
                            #'biosamples': { 'returnEntryType': 'biosample', 'url': '{}/api/individuals/"target_id_req"/biosamples'.format( config.server_api_url ) }
                        }
                    },
                    'individual': {
                        'entryType': 'individual',
                        'rootUrl': '{}api/individuals'.format( config.server_api_url ),
                        'singleEntryUrl': '{}api/individuals/"id"'.format( config.server_api_url ),
                        'endpoints': {}
                    }
                }
            }
        }
        return await json_response( request, rsp )
    return wrapper

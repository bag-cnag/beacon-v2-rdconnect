#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import logging

from server.config import config
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


def map(request):
    async def wraper(request):
        map = {
            'title': 'Beacon Map',
            'description': 'Map of a Beacon, its entry types and endpoints. It is conceptually similar to a website sitemap.',
            'endpointSets': {
                'biosamples': {
                    'entryType': 'biosample',
                    'rootUrl': '{}/biosamples'.format(config.server_api_url),
                    'singleEntryUrl': '{}/biosamples/\{id\}'.format(config.server_api_url)
                },
                'individuals': {
                    'entryType': 'individual',
                    'rootUrl': '{}/individuals'.format(config.server_api_url),
                    'singleEntryUrl': '{}/individuals/\{id\}'.format(config.server_api_url),
                }
            }
        }
        return await map
    return wraper


def configuration(request):
    async def wraper(request):
        configuration = {
            'maturityAttributes': {
                'productionStatus': '{}/'.format(config.environment, config.api_version)
            },
            'securityAttributes': {
                'defaultGranularity': 'boolean',
                'securityLevels': ['{}'.format(config.security)]
            },
            'entryTypes': {
                'individual': {
                    'individualId': 'individual',
                    'aCollectionOf': {
                        'individualId': 'id',
                        'sex': ['Female', 'Male'],
                        'phenotypicFeatures': [{'id': 'HP:0000000', 'name': 'HP:term', 'observed': [False, True] }],
                        'diseases': [{ 'ordo': { 'id': 'Orphanet:000000', 'name': 'Orphanet:term' } }],
                        'measures': [{ 'curves': '', 'height': '', 'weight': '', 'head_circ': '', 'measurement_date': '1987-11-26' }],
                        'info': { 'family': 'AAA0000000', 'index': ['No', 'Yes'], 'solved': ['Solved', 'Unsolved'], 'iid': 'RD-Connect GPAP ID' }
                    },    
                    'partOfSpecification': 'Beacon v2.0-draft3',
                    'description': 'An individual is the definition of a human participant in RD-Connect and Solve-RD.',
                    'defaultSchema': {
                        'id': 'datasetDefaultSchema',
                        'name': 'Default schema for individual',
                        'schemaVersion': 'v.2.draft-3'
                    },
                    'endpoint': 'api/individuals'
                },
                'biosamples': {
                    'biosampleId': 'biosample',
                    'aCollectionOf': {
                        'biosampleId': 'id',
                        'subjectId': 'individualId',
                        'info': {
                            'owner': 'ownerTag',
                            'tissue': 'tissueByStr',
                            'ega_id': ['EgaId', 'null'],
                            'in_platform': [False, True],
                            'experiment_type': ['WES', 'WGS'],
                            'library_source': ['...', 'Other'],
                            'library_selection': ['...', 'unspecified'],
                            'library_strategy': ['WES', 'WGS'],
                            'library_contruction_protocol': ['...', 'null'],
                            'POSTEMBARGO': [False, True],
                            'kit': ['...', 'null'],
                            'tumour_experiment_id': ['pairedTumorId', 'null']
                        }
                    },    
                    'partOfSpecification': 'Beacon v2.0-draft3',
                    'description': 'An biosample is the experiment corresponding to an individual who participanted in RD-Connect and Solve-RD.',
                    'defaultSchema': {
                        'id': 'datasetDefaultSchema',
                        'name': 'Default schema for biosample',
                        'schemaVersion': 'v.2.draft-3'
                    },
                    'endpoint': 'api/biosamples'
                }
            }
        }
        return configuration
    return wraper
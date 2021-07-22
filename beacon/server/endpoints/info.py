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
        print('hello')
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
                    'singleEntryUrl': '{}/biosamples/"id"'.format(config.server_api_url)
                },
                'individuals': {
                    'entryType': 'individual',
                    'rootUrl': '{}/individuals'.format(config.server_api_url),
                    'singleEntryUrl': '{}/individuals/"id"'.format(config.server_api_url),
                }
            }
        }
        return await json_response(request, map)
    return wraper


def config_txt(request):
    async def wraper(request):
        txt = {
            'maturityAttributes': {
                'productionStatus': '{}/{}'.format(config.environment, config.api_version)
            },
            'securityAttributes': {
                'description': 'Default granularity. Some responses could return higher detail, but this would be the granularity by default.- `boolean`: returns "true/false" responses.\n\n - `count`: adds the total number of positive results found.\n\n - `aggregated`: returns summary, aggregated or distribution like responses.\n\n. - `record`: returns details for every row. The cases where a Beacon prefers to return records with less, not all attributes, different strategies have been considered, e.g.: keep non-mandatory attributes empty, or Beacon to provide a minimal record definition, but these strategies still need to be tested in real world cases and hence no design decision has been taken yet.\n\n',
                'defaultGranularity': 'record',
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
        return await json_response(request, txt)
    return wraper


def entry_types(request):
    async def wrapper(request):
        rsp = {
            'title': 'Entry Types',
            'description': 'Definition of an element or entry type including the Beacon v2 required and suggested attributes. This schema purpose is to  describe each type of entities included in a Beacon, hence Beacon clients could have some metadata about such entities.\n\nThe ìd`attribute is the key that should be used in other parts of the Beacon Model to allow Beacon clients to identify the different parts (e.g. endpoints, filteringTerms, request parameters, etc.) that fully describe an entry type.',
            'properties': {
                'id': {
                    '$comments': '++++++ THIS IS THE START OF THE ontologized element ++++++',
                    'type': 'string',
                    'description': 'A (unique) identifier of the element.'
                },
                'name': {
                    'type': 'string',
                    'description': 'A distinctive name for the element.'
                },
                'description': {
                    'type': 'string',
                    'description': 'A textual description for the element.'
                },
                'partOfSpecification': {
                    'description': 'This is label to group together entry types that are part of the same specification.',
                    'type': 'string',
                    'example': 'Beacon v2.0-draft3'
                },
                'defaultSchema': {
                    'description': 'Description of the default schema used for this concept.',
                },
                'additionallySupportedSchemas': {
                    'description': 'List of additional schemas that could be used for this concept in this instance of Beacon.',
                    'type': 'array'
                },
                'aCollectionOf': {
                    'description': 'If the entry type is a collection of other entry types, (e.g. a Dataset is a collection of Records), then this attribute must list the entry types that could be included. One collection type could be defined as included more than one entry type (e.g. a Dataset could include Individuals or Genomic Variants), in such cases the entries are alternative, meaning that a given instance of this entry type could be of only one of the types (e.g. a given Dataset contains Individuals, while another Dataset could contain Genomic Variants, but not both at once).',
                    'includedConcepts': {
                        'type': 'array'
                    }
                },
                'filteringTerms': {
                    'description': 'Reference to the file with the list of filtering terms that could be used to filter this concept in this instance of Beacon. The referenced file could be used to populate the `filteringTerms`endpoint. Having it independently should allow for updating the list of accepted filtering terms when it is necessary.',
                    'type': 'string'
                }
            },
            'required': [
                'id',
                'name',
                'ontologyTermForThisType',
                'partOfSpecification',
                'defaultSchema'
            ],
            'additionalProperties': True
        }
        return await json_response(request, rsp)
    return wrapper

def filtering_terms(request):
    async def wrapper(request):
        rsp = {
            'title': 'Filtering Terms schema',
            'description': 'Schema for the Filtering Terms list related to the hosting entry type. It is kept separated to allow updating it independently.',
            'type': 'object',
            'properties': {
                'filteringTerms': {
                    'description': 'List of filtering terms that could be used to filter this concept in this instance of Beacon.',
                    'type': 'array',
                    'minItems': 0
                }
            },
            'required': ['filteringTerms'],
            'additionalProperties': True
        }
        return await json_response(request, rsp)
    return wrapper
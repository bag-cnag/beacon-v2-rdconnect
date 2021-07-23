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
                'dataset': {
                    'entryType': 'dataset',
                    'rootUrl': '{}/datasets'.format(config.server_api_url),
                    'singleEntryUrl': '{}/datasets/"id"'.format(config.server_api_url),
                    'endoints': {}
                },
                'biosample': {
                    'entryType': 'biosample',
                    'rootUrl': '{}/biosamples'.format(config.server_api_url),
                    'singleEntryUrl': '{}/biosamples/"id"'.format(config.server_api_url),
                    'endoints': {
                        'biosamples': {'returnEntryType': 'biosample', 'url': '{}/api/individuals/"target_id_req"/biosamples'.format(config.server_api_url)}
                    }
                },
                'individual': {
                    'entryType': 'individual',
                    'rootUrl': '{}/individuals'.format(config.server_api_url),
                    'singleEntryUrl': '{}/individuals/"id"'.format(config.server_api_url)
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
                "dataset": {
                    "id": "dataset",
                    "name": "Dataset",
                    "ontologyTermForThisType": {
                        "id": "NCIT:C47824",
                        "label": "Data set"
                    },
                    "partOfSpecification": "Beacon v2.0.0-draft.4",
                    "description": "A Dataset is a collection of records, like rows in a database or cards in a cardholder.",
                    "defaultSchema": {
                        "id": "ga4gh-beacon-dataset-v2.0.0-draft.4",
                        "name": "Default schema for datasets",
                        "referenceToSchemaDefinition": "./datasets/defaultSchema.json",
                        "schemaVersion": "v2.0.0-draft.4"
                    },
                    "aCollectionOf": [{ "id": "individual", "name": "Individuals" }],
                    "additionalSupportedSchemas": []
                },
                "individual": {
                    "id": "individual",
                    "name": "Individual",
                    "ontologyTermForThisType": {
                        "id": "NCIT:C25190",
                        "label": "Person"
                    },
                    "partOfSpecification": "Beacon v2.0.0-draft.4",
                    "description": "A human being. It could be a Patient, a Tissue Donor, a Participant, a Human Study Subject, etc.",
                    "defaultSchema": {
                        "id": "ga4gh-beacon-individual-v2.0.0-draft.4",
                        "name": "Default schema for an individual",
                        "referenceToSchemaDefinition": "./individuals/defaultSchema.json",
                        "schemaVersion": "v2.0.0-draft.4"
                    },
                    "additionallySupportedSchemas": []
                },
                "biosample": {
                    "id": "biosample",
                    "name": "Biological Sample",
                    "ontologyTermForThisType": {
                        "id": "NCIT:C70699",
                        "label": "Biospecimen"
                    },
                    "partOfSpecification": "Beacon v2.0.0-draft.4",
                    "description": "Any material sample taken from a biological entity for testing, diagnostic, propagation, treatment or research purposes, including a sample obtained from a living organism or taken from the biological object after halting of all its life functions. Biospecimen can contain one or more components including but not limited to cellular molecules, cells, tissues, organs, body fluids, embryos, and body excretory products. [ NCI ]",
                    "defaultSchema": {
                        "id": "ga4gh-beacon-biosample-v2.0.0-draft.4",
                        "name": "Default schema for a biological sample",
                        "referenceToSchemaDefinition": "./biosamples/defaultSchema.json",
                        "schemaVersion": "v2.0.0-draft.4"
                    },
                    "additionallySupportedSchemas": []
                }
            }
        }
        return await json_response(request, txt)
    return wraper


def entry_types(request):
    async def wrapper(request):
        rsp = {
            '$schema': 'https://raw.githubusercontent.com/ga4gh-beacon/beacon-framework-v2/main/responses/beaconEntryTypesResponse.json',
            'meta': {
                'beaconId':	'org.ga4gh.beacon',
                'apiVersion': 'v2.0-draft4',
                'returnedSchemas':	[	
                    { 'entryTypes': 'beacon-entry-types-v2.0.0-draft.3' }
                ]
            },
            'response': {
                '$schema': 'https://raw.githubusercontent.com/ga4gh-beacon/beacon-framework-v2/main/configuration/entryTypesSchema.json',
                'entryTypes': {
                    'dataset': {
                        'id': 'dataset',
                        'name': 'Dataset',
                        'ontologyTermForThisType': {
                            'id': 'NCIT:C47824',
                            'label': 'Data set'
                        },
                        'partOfSpecification': 'Beacon v2.0.0-draft.4',
                        'description': 'A Dataset is a collection of individuals.',
                        'defaultSchema': {
                            'id': 'ga4gh-beacon-dataset-v2.0.0-draft.4',
                            'name': 'Default schema for datasets',
                            'referenceToSchemaDefinition': './datasets/defaultSchema.json',
                            'schemaVersion': 'v2.0.0-draft.4'
                        },
                        'aCollectionOf': [{
                            'id': 'genomicVariant',
                            'name': 'Genomic Variants'
                        }],
                        'additionalSupportedSchemas': []
                    }
                }
            }
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
                    'minItems': 0
                }
            },
            'required': ['filteringTerms'],
            'additionalProperties': True
        }
        return await json_response(request, rsp)
    return wrapper
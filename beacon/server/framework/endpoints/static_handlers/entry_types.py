#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from server.config import config
from server.logger import LOG
from server.framework.utils import json_response

#def entry_types( request ):
def entry_types():
    async def wrapper( request ):
        LOG.debug( 'Running a GET "entry_types" request' )
        rsp = {
            'meta': {
                'beaconId':	config.beacon_id,
                'apiVersion': config.api_version,
                'returnedSchemas':	[	
                    {
                        'entityType': 'entryType',
                        'schema': 'https://raw.githubusercontent.com/ga4gh-beacon/beacon-framework-v2/main/configuration/entryTypesSchema.json',
                    }
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
                        'aCollectionOf': [ {
                            'id': 'individuals',
                            'name': 'GPAP Participants'
                        } ],
                        'additionalSupportedSchemas': [ ]
                    },
                    'individual': {
                        'id': 'individual',
                        'name': 'GPAP Participants',
                        'ontologyTermForThisType': {
                            'id': 'NCIT:C25190',
                            'label': 'Person'
                        },
                        'partOfSpecification': 'Beacon v2.0.0-draft.4',
                        'description': 'An individual is a person, participant, with WES or WGS information in RD-Connect GPAP.',
                        'defaultSchema': {
                            'id': 'ga4gh-beacon-individual-v2.0.0-draft.4',
                            'name': 'Default schema for individuals',
                            'referenceToSchemaDefinition': './individuals/defaultSchema.json',
                            'schemaVersion': 'v2.0.0-draft.4'
                        },
                        'aCollectionOf': [ {
                            'id': 'biosamples',
                            'name': 'Virtual collection of GPAP experiments'
                        } ],
                        'additionalSupportedSchemas': [ ]
                    },
                    'biosample': {
                        'id': 'biosample',
                        'name': 'Collection of GPAP experiments',
                        'ontologyTermForThisType': {
                            'id': 'NCIT:C43412',
                            'label': 'Biosample'
                        },
                        'partOfSpecification': 'Beacon v2.0.0-draft.4',
                        'description': 'A biosample is a virtual individual that contains a collection of RD-Connect WES or WGS experiments.',
                        'defaultSchema': {
                            'id': 'ga4gh-beacon-biosample-v2.0.0-draft.4',
                            'name': 'Default schema for biosample',
                            'referenceToSchemaDefinition': './biosample/defaultSchema.json',
                            'schemaVersion': 'v2.0.0-draft.4'
                        },
                        'additionalSupportedSchemas':  [ ]
                    }
                }
            }
        }
        return await json_response( request, rsp )
    return wrapper

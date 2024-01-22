#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from server.config import config
from server.logger import LOG
from server.framework.utils import json_response


#def config_txt( request ):
def config_txt():
    async def wrapper( request ):
        LOG.debug( 'Running a GET "config_txt" request' )
        rsp = {
            'meta': {
                'beaconId':	config.beacon_id,
                'apiVersion': 'v2.0-draft4',
                'returnedSchemas': [ {
                    'entityType': 'map',
                    'schema': 'https://raw.githubusercontent.com/ga4gh-beacon/beacon-framework-v2/main/responses/beaconConfigurationResponse.json',
                } ],
            },
            'response': {
                '$schema': 'https://raw.githubusercontent.com/ga4gh-beacon/beacon-framework-v2/main/responses/beaconConfigurationResponse.json',
                'maturityAttributes': {
                    'productionStatus': '{}'.format( config.production_status )
                },
                'securityAttributes': {
                    'description': 'Default granularity. Some responses could return higher detail, but this would be the granularity by default.- `boolean`: returns "true/false" responses.\n\n - `count`: adds the total number of positive results found.\n\n - `aggregated`: returns summary, aggregated or distribution like responses.\n\n. - `record`: returns details for every row. The cases where a Beacon prefers to return records with less, not all attributes, different strategies have been considered, e.g.: keep non-mandatory attributes empty, or Beacon to provide a minimal record definition, but these strategies still need to be tested in real world cases and hence no design decision has been taken yet.\n\n',
                    'defaultGranularity': 'record',
                    'securityLevels': [ '{}'.format( config.security ) ]
                },
                'entryTypes': {
                    'dataset': {
                        'id': 'dataset',
                        'name': 'Dataset',
                        'ontologyTermForThisType': {
                            'id': 'NCIT:C47824',
                            'label': 'Data set'
                        },
                        'partOfSpecification': 'Beacon v2.0.0-draft.4',
                        'description': 'A Dataset is a collection of records, like rows in a database or cards in a cardholder.',
                        'defaultSchema': {
                            'id': 'ga4gh-beacon-dataset-v2.0.0-draft.4',
                            'name': 'Default schema for datasets',
                            'referenceToSchemaDefinition': './datasets/defaultSchema.json',
                            'schemaVersion': 'v2.0.0-draft.4'
                        },
                        'aCollectionOf': [ { 'id': 'individual', 'name': 'Individuals' } ],
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
                        'additionallySupportedSchemas': [ ]
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

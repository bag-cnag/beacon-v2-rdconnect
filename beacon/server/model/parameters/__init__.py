#!/usr/bin/env python3
# -*- coding: utf-8 -*-


from multidict import MultiDict

import server.model.parameters.validators as valid
from server.logger import LOG
from server.framework.exceptions import BeaconBadRequest
from server.model.schemas import supported_schemas_by_entity



# response
#current_page
#next_page
#previous_page


async def process_request(request, entity):
    default_params = {
        'meta': {
            'apiVersion'           : 'v2.0.0-draft.4',
        },
        'query': {
            'pagination'           : { 'skip': 1, 'limit': 5 },
            'requestedGranularity' : 'count', #["boolean", "count", "aggregated", "record"]
            'requestedSchemas'      : [ { 'entityType': entity, 'schema': supported_schemas_by_entity[ entity ] } ]
        },
    }

    if request.headers.get('Content-Type') == 'application/json':
        qrt = MultiDict(await request.json())
    else:
        qrt = MultiDict(await request.post())
    
    print(qrt, request, entity)

    if 'meta' not in qrt:
        qrt.add( 'meta', default_params[ 'meta' ] )
    else:
        if 'apiVersion' not in qrt[ 'meta' ]:
            qrt[ 'meta' ][ 'apiVersion' ] = default_params[ 'meta' ][ 'apiVersion' ]
    
    if 'query' not in qrt:
        qrt.add( 'query', default_params[ 'query' ] )
    else:
        if 'pagination' not in qrt[ 'query' ]:
            qrt[ 'query' ][ 'pagination' ] = default_params[ 'query' ][ 'pagination' ]
        if 'requestedGranularity' not in qrt[ 'query' ]:
            qrt[ 'query' ][ 'requestedGranularity' ] = default_params[ 'query' ][ 'requestedGranularity' ]
        if 'requestedSchemas' not in qrt[ 'query' ]:
            qrt[ 'query' ][ 'requestedSchemas' ] = default_params[ 'query' ][ 'requestedSchemas' ]
        else:
            if len( qrt[ 'query' ][ 'requestedSchemas' ] ) > 1:
                raise BeaconBadRequest( 'Expected single item in requested schemas but more were received.')
            if qrt[ 'query' ][ 'requestedSchemas' ] != supported_schemas_by_entity[ entity ]:
                raise BeaconBadRequest( 'For entity "{}", this beacon supports "{}" but not "{}".'.format( entity, supported_schemas_by_entity[ entity ], qrt[ 'query' ][ 'requestedSchemas' ]))
    
    return qrt


# def build(entity, map, qrt):
#     rst = {}
#     for key in map.keys():
#         if key in qrt.keys():
#             rst[key] = map[key]['valid'](qrt[key])
#         elif key not in qrt.keys() and map[key]['required']:
#             raise BeaconBadRequest('Expected argument "{}" in section "{}" from request.'.format(key, entity))
#     return rst















# filters = {
#     'datasets': {
#         'requestedSchema'               : { 'default': 'beacon-dataset-v2.0.0-draft.4' },
#     },
#     'cohorts': {
#         'requestedSchema'               : { 'default': 'beacon-cohort-v2.0.0-draft.4' },
#     },
#     'biosamples': {
#         'requestedSchema'               : { 'default': 'beacon-biosample-v2.0.0-draft.4' },
#         'RD_Connect_ID_Experiment'      : 'string',
#         'Participant_ID'                : 'string',
#         'EGA_ID'                        : 'string',
#         'Owner'                         : 'string',
#         'in_platform'                   : 'bool',
#         'POSTEMBARGO'                   : 'bool',
#         'experiment_type'               : 'string',
#         'kit'                           : 'string',
#         'tissue'                        : 'string',
#         'library_source'                : 'string',
#         'library_selection'             : 'string',
#         'library_strategy'              : 'string',
#         'library_contruction_protocol'  : 'string',
#         'erns'                          : 'string',
#     },
#     'individuals': {
#         'requestedSchema'               : { 'default': 'beacon-individual-v2.0.0-draft.4' },
#         'id'                            : 'string',
#         'family_id'                     : 'string' ,
#         'index'                         : 'string',
#         'solved'                        : 'string',
#         'sex'                           : 'string',
#         'affectedStatus'                : 'string',
#         'lifeStatus'                    : 'string',
#     }
# }



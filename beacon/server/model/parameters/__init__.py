#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import server.model.parameters.validators as valid
from server.logger import LOG
from server.framework.exceptions import BeaconBadRequest
from server.model.schemas import supported_schemas_by_entity

async def process_request(request, entity):
    global params
    if request.headers.get('Content-Type') == 'application/json':
        qrt = await request.json()
    else:
        qrt = await request.post()

    meta = build('meta', params['meta'], qrt['meta'])
    if 'requestedSchemas' not in meta.keys():
        meta['requestedSchemas'] = [ { 'entity': entity, 'schema': supported_schemas_by_entity['entity'] } ]
    query = build('query', params['query'], qrt['query'])

    LOG.debug('Processed request (meta + query)')
    return { **meta , **query }


def build(entity, map, qrt):
    rst = {}
    for key in map.keys():
        if key in qrt.keys():
            rst[key] = map[key]['valid'](qrt[key])
        elif key not in qrt.keys() and map[key]['required']:
            raise BeaconBadRequest('Expected argument "{}" in section "{}" from request.'.format(key, entity))
    return rst


params = {
    'meta': {
        'apiVersion'                    : { 'valid': valid.api_version, 'required': True },
        'requestedSchemas'              : { 'valid': valid.requested_schemas, 'required': False },
    },
    'query': {
        'filters'                       : { 'valid': valid.filters, 'required': False },
        'pagination'                    : { 'valid': valid.pagination, 'required': False },
        'requestedGranularity'          : { 'valid': valid.requested_granularity, 'required': False },
    },
}












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



#!/usr/bin/env python3
# -*- coding: utf-8 -*-


from multidict import MultiDict

import server.model.parameters.validators as valid
from server.logger import LOG
from server.config import config
from server.framework.exceptions import BeaconBadRequest
from server.model.schemas import supported_schemas_by_entity



async def process_request( request, entity ):
    default_params = {
        'meta': {
            'apiVersion'           : 'v2.0.0-draft.4',
            'requestedSchemas'     : [ { 'entityType': entity, 'schema': supported_schemas_by_entity[ entity ] } ],
        },
        'query': {
            'pagination'           : { 'skip': 1, 'limit': 5 },
            'requestedGranularity' : 'count', #["boolean", "count", "aggregated", "record"]
            'filters'              : [],
        },
        'targetIdReq'              :  request.match_info.get('target_id_req')
    }
    # Get query from json or from plain
    if request.headers.get('Content-Type') == 'application/json':
        qrt = MultiDict( await request.json() )
    else:
        qrt = MultiDict( await request.post() )
    # Add the targetIdReq
    qrt.add( 'targetIdReq', default_params[ 'targetIdReq' ] )
    # If no meta, add the default meta (apiVersion)
    # If meta, check that apiVersion is added an dif not we add it
    if 'meta' not in qrt:
        qrt.add( 'meta', default_params[ 'meta' ] )
    else:
        if 'apiVersion' not in qrt[ 'meta' ]:
            qrt[ 'meta' ][ 'apiVersion' ] = default_params[ 'meta' ][ 'apiVersion' ]
        if 'requestedSchemas' not in  qrt[ 'meta' ]:
            qrt[ 'meta' ][ 'requestedSchemas' ] = default_params[ 'meta' ][ 'requestedSchemas' ]
    # If no query, add query with pagination, granularity, and schema
    # If query, check that the elements are there and if not add them.
    # If query, check that the schema requested is available and if not raise error
    # If filters, validate them and if not raise error
    if 'query' not in qrt:
        qrt.add( 'query', default_params[ 'query' ] )
    else:
        if 'pagination' not in qrt[ 'query' ]:
            qrt[ 'query' ][ 'pagination' ] = default_params[ 'query' ][ 'pagination' ]
        if 'requestedGranularity' not in qrt[ 'query' ]:
            qrt[ 'query' ][ 'requestedGranularity' ] = default_params[ 'query' ][ 'requestedGranularity' ]
        else:
            if len( qrt[ 'meta' ][ 'requestedSchemas' ] ) > 1:
                raise BeaconBadRequest( 'Expected single item in requested schemas but more were received.')
            if qrt[ 'meta' ][ 'requestedSchemas' ][ 0 ][ 'schema' ] != supported_schemas_by_entity[ entity ]:
                raise BeaconBadRequest( 'For entity "{}", this beacon supports "{}" but not "{}".'.format( entity, supported_schemas_by_entity[ entity ], qrt[ 'meta' ][ 'requestedSchemas' ][ 0 ][ 'schema' ] ) )
        if 'filters' not in qrt[ 'query' ]:
            qrt[ 'query' ][ 'filters' ] = default_params[ 'query' ][ 'filters' ]
        else:
            flag, err, filters = validate_filters( qrt[ 'query' ][ 'filters' ], entity )
            if flag: 
                print (filters)
                if ("id" in err) and (err["id"] == "unsupported_filter"):
                    qrt[ 'query' ][ 'unsupportedFilters' ] = filters

                #qrt[ 'query' ][ 'filters' ] = filters
            else:
                raise BeaconBadRequest( err ) 
    # TODO 
    # check if more than one entity was given in the body
    return qrt


def validate_filters( filters, entity ):
    # Check that all filters provide scope
    if sum( [ 'scope' in x.keys() for x in filters ] ) != len( filters ):
        return False, 'Some of the provided filters do not indicate their scope.', [ ]

    # check scope - for now only individuals filters can be used
    # if sum( [ x['scope'] == 'individuals' for x in filters ] ) != len( filters ):
    #     return False, 'Currently, this beacon only accepts filters for "individuals".', [ ]
    # check that all the filters are valid filters

    unsupported_types = []

    for x in filters:
        if entity == 'individuals':

            '''Check if and how to validate HPOs ORDO & OMIM terms'''
            #if not x[ 'id' ] in config.filters_in[ 'hpos' ] and not x[ 'id' ] in config.filters_in[ 'ordos' ] and not x[ 'id' ] in config.filters_in[ 'sex' ]:
            #    return False, 'Provided fiters "{}" for scope "{}" is not available.'.format( x[ 'id' ], x[ 'scope' ] ), [ ]

            if x['id'].startswith('NCIT') and not x['id'] in config.filters_in['sex']:
                return False, 'Provided fiters "{}" for scope "{}" is not available.'.format( x[ 'id' ], x[ 'scope' ] ), [ ]

            #Check type and if is supported
            if "type" in x and x["type"] in config.filters_in["unsupported_type_terms"]:
                unsupported_types.append(x["type"])

        if entity == 'biosamples':
            if not x[ 'id' ] in config.filters_in[ 'tech' ] and not x[ 'id' ] in config.filters_in[ 'erns' ]:
                return False, 'Provided fiters "{}" for scope "{}" is not available.'.format( x[ 'id' ], x[ 'scope' ] ), [ ]
    
    #Unsupported types
    if len(unsupported_types) > 0:
        return True, {"id": "unsupported_filter"}, unsupported_types

    # remove filters that do not apply
    filters = [ x[ 'id' ] for x in filters if x[ 'scope' ] ==  entity ]
    return True, '', filters

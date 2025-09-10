#!/usr/bin/env python3
# -*- coding: utf-8 -*-


from multidict import MultiDict

import server.model.parameters.validators as valid
from server.logger import LOG
from server.config import config
from server.framework.exceptions import BeaconBadRequest
from server.model.schemas import supported_schemas_by_entity



async def process_request( request, entity ):

    if entity == "variants" : entity = "genomicVariant"

    default_params = {
        'meta': {
            'apiVersion'           : 'v2.0.0',
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
            flag, err, filters = validate_filters( qrt[ 'meta' ][ 'apiVersion' ], qrt[ 'query' ][ 'filters' ], entity )
            if flag: 
                #print (filters)
                if ("id" in err) and (err["id"] == "unsupported_filter"):
                    qrt[ 'query' ][ 'unsupportedFilters' ] = filters

                #qrt[ 'query' ][ 'filters' ] = filters
            else:
                raise BeaconBadRequest( err ) 
    # TODO 
    # check if more than one entity was given in the body
    return qrt


def validate_filters(api_version, filters, entity ):
    
    '''Scope will be optional, so no check here'''
    # Check that all filters provide scope
    #if sum( [ 'scope' in x.keys() for x in filters ] ) != len( filters ):
    #    return False, 'Some of the provided filters do not indicate their scope.', [ ]

    # check scope - for now only individuals filters can be used
    # if sum( [ x['scope'] == 'individuals' for x in filters ] ) != len( filters ):
    #     return False, 'Currently, this beacon only accepts filters for "individuals".', [ ]
    # check that all the filters are valid filters

    unsupported_types = []

    '''Provide error for unsupported apiVersion'''
    #if api_version != "v0.1" and api_version != "v0.2":
    #    return False, 'Provided apiVersion "{}" is not supported (provide one from: [v0.1, v0.2])'.format(api_version), [ ]

    #Check requested api version
    if api_version == "v0.1":
        filter_key = "type"
    else:
        filter_key = "id"

    for x in filters:
        if entity == 'individuals':

            '''Check if and how to validate HPOs ORDO & OMIM terms'''
            #if not x[ 'id' ] in config.filters_in[ 'hpos' ] and not x[ 'id' ] in config.filters_in[ 'ordos' ] and not x[ 'id' ] in config.filters_in[ 'sex' ]:
            #    return False, 'Provided fiters "{}" for scope "{}" is not available.'.format( x[ 'id' ], x[ 'scope' ] ), [ ]
            
            '''Check if and how to validate sex NCIT values'''
            #if (x['id'].startswith('NCIT') or x['id'].startswith('obo:NCIT'))  and not x['id'] in config.filters_in['sex']:
            #    return False, 'Provided filter "{}"  is not available.'.format( x[ 'id' ]), [ ]
              
            #Check sex if it is alphanumeric as in EJP
            if (x['id'] == "NCIT_C28421" or x['id'] == "NCIT:C28421" or x['id'] == "ncit:C28421")  and not x['value'] in config.filters_in['sex']:
                return False, 'Provided filter "{}"  is not available.'.format( x[ 'value' ]), [ ]

            #Check type and if is supported
            if (filter_key in x) and (x[filter_key] not in (config.filters_in["individuals_supported_type_terms"])) and ("orpha" not in str(x[filter_key]).lower()) and ("hp" not in str(x[filter_key]).lower()):
                unsupported_types.append(x[filter_key])

        if entity == 'biosamples':
            if 'value' in x and not x[ 'value' ] in config.filters_in[ 'tech' ] and not x[ 'value' ] in config.filters_in[ 'erns' ]:
                return False, 'Provided filters "{}"  is not available.'.format( x[ 'value' ]), [ ]
            
            #Check type and if is supported
            if (filter_key in x) and (x[filter_key] not in (config.filters_in["biosamples_supported_type_terms"])):
                unsupported_types.append(x[filter_key])
    
    #Unsupported types
    if len(unsupported_types) > 0:
        return True, {"id": "unsupported_filter"}, unsupported_types

    # remove filters that do not apply
    #filters = [ x[ 'id' ] for x in filters if x[ 'scope' ] ==  entity ]
    filters = [ x[ 'id' ] for x in filters ]

    return True, '', filters

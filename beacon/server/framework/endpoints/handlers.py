#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import jwt
from server.config import config
from server.framework.utils import json_response
from server.framework.exceptions import  BeaconServerError, BeaconForbidden, BeaconEndPointNotImplemented
from server.framework.response import build_beacon_response, build_variant_response, build_variant_v1_response
from server.gpap import get_kc_token
from server.logger import LOG

from server.model.parameters import process_request

jwt_options = config.jwt_options
jwt_algorithm = config.jwt_algorithm
public_key  = '-----BEGIN PUBLIC KEY-----\n' + config.beacon_idrsa + '\n-----END PUBLIC KEY-----'

def test( entity ):
    async def wrapper( request) :
        LOG.debug( '{} - Test endpoint'.format( request.method ) )
        response = { 'result': 'this is a test' }
        return await json_response( request, response )
    return wrapper


def _extract_items( token,name) :
    if token.get( name ) is not None:
        return [ s.replace( '/', '' ) for s in token.get( name ) ]
    else:
        return []


# ('datasets' , _datasets_proxy, fetch_datsets_by_dataset, build_dataset_response)
def generic( entity, fetch_func, build_response_func ):
    async def wrapper( request ):
        LOG.info( 'Running a request for {}'.format( entity ) )
        access_token = request.headers.get( 'auth-key' )
        
        if not access_token and config.gpap_token_required[ 0 ]:
            LOG.debug( 'No access token but validation required.' )
            raise BeaconForbidden( error = 'No authentication header or wrong header name was provided' )
        elif not config.gpap_token_required[ 0 ]:
            LOG.debug( 'No access token and validation not required.' )
            access_token = get_kc_token()[ 'access_token' ]
        else:
            LOG.debug( 'Access token received.' )
            #access_token = access_token[ 7: ]

        try:
            decoded  = jwt.decode (access_token, public_key, algorithms = jwt_algorithm, options = jwt_options )
            LOG.debug( 'Token was decoded' )
            groups   = _extract_items( decoded, 'group' )
            projects = _extract_items( decoded, 'group_projects' )
        except Exception as e:
            print( 'Exception', e )
            LOG.debug( 'Invalid validation of token. {}'.format( str( e ) ) )
            raise BeaconServerError( error = 'Invalid validation of token. {}.'.format( str( e ) ) )

        if len( projects ) == 0:
            projects.append( 'no_project' )

        qparams = await process_request( request, entity )

        #######################################################################################
        # In RD-Connect each 'experiment' is a 'dataset', therefore it makes no sense to check
        # for dataset access since if the user asks for an individual or an experiment
        # that has no access GPAP returns empty.
        #######################################################################################
        #non_accessible_datasets = []
        num_total_results, response = fetch_func( qparams, access_token, groups, projects )
        
        # Create reponse
        #rows = [row async for row in response]
        #rows = [row for row in response]
        #num_total_results = await response_total_results
        #response_converted = build_beacon_response(proxy, response, num_total_results, qparams, entity, non_accessible_datasets, build_response_func)
        response_converted = build_beacon_response( entity, qparams, num_total_results, response, build_response_func )
        
        LOG.info( 'Formatting the response for %s', entity )
        return await json_response( request, response_converted )
    return wrapper

def not_implemented(entity):
    async def wrapper(request):
        LOG.info('Running a request for %s (not implemented)', entity)
        """
        access_token = request.headers.get('Authorization')
        if access_token:
            access_token = access_token[7:]
            try:
                decoded = jwt.decode(access_token, public_key, algorithms = 'RS256', options = jwt_options)
                userid   = decoded.get('preferred_username')
            except Exception as e:
                raise BeaconServerError(error = str(e))
        else:
            raise BeaconForbidden(error = 'No authentication header was provided')
        """
        raise BeaconEndPointNotImplemented() 
    return wrapper



# ('datasets' , _datasets_proxy, fetch_datsets_by_dataset, build_dataset_response)
def handler_fixed_token( entity, fetch_func, build_response_func ):
    async def wrapper( request ):
        LOG.info( 'Running a request for {}'.format( entity ) )
        access_token = request.headers.get( 'auth-key' )
        
        if not access_token and config.gpap_token_required[ 0 ]:
            LOG.debug( 'No access token but validation required.' )
            #raise BeaconForbidden( error = 'No authentication header or wrong header name was provided' )
        elif not config.gpap_token_required[ 0 ]:
            LOG.debug( 'No access token and validation not required.' )
            access_token = get_kc_token()[ 'access_token' ]
        else:
            LOG.debug( 'Access token received.' )
            #access_token = access_token[ 7: ]

        try:
            decoded  = jwt.decode (access_token, public_key, algorithms = jwt_algorithm, options = jwt_options )
            groups   = _extract_items( decoded, 'group' )
            projects = _extract_items( decoded, 'group_projects' )
            roles =  _extract_items( decoded, 'realm_access' )
            
            #Possible roles: full_access, count_access, boolean_access
            roles = ["count_access"]

            print (groups)
            print (projects)
            print (roles)
            
            LOG.debug( 'Token was decoded' )
            #groups = "beacon"
            #projects = "beacon"
            
        except Exception as e:
            print( 'Exception', e )
            LOG.debug( 'Invalid validation of token. {}'.format( str( e ) ) )
            raise BeaconServerError( error = 'Invalid validation of token. {}.'.format( str( e ) ) )

        if len( projects ) == 0:
            projects.append( 'no_project' )

        qparams = await process_request( request, entity )

        #num_total_results, response, gamw = fetch_func( qparams, access_token, groups, projects, request )
        all_data = fetch_func( qparams, access_token, groups, projects, roles, request )

        print (all_data)
        
        # Create reponse
        response_converted = build_beacon_response( entity, qparams, build_response_func, all_data )
        
        LOG.info( 'Formatting the response for %s', entity )
        return await json_response( request, response_converted )
    return wrapper



# Beacon v1
def handler_variants( entity, fetch_func, build_response_func ):
    async def wrapper( request ):
        LOG.info( 'Running a request for {}'.format( entity ) )

        access_token = request.headers.get( 'auth-key' )
        #access_token = "beaconv1"
                
        if not access_token and config.gpap_token_required[ 0 ]:
            LOG.debug( 'No access token but validation required.' )
            #raise BeaconForbidden( error = 'No authentication header or wrong header name was provided' )
        elif not config.gpap_token_required[ 0 ]:
            LOG.debug( 'No access token and validation not required.' )
            access_token = get_kc_token()[ 'access_token' ]
        else:
            LOG.debug( 'Access token received.' )
            #access_token = access_token[ 7: ]

        try:
            #decoded  = jwt.decode (access_token, public_key, algorithms = jwt_algorithm, options = jwt_options )
            #groups   = _extract_items( decoded, 'group' )
            #projects = _extract_items( decoded, 'group_projects' )
            
            LOG.debug( 'Token was decoded' )
            groups = "beacon"
            projects = "beacon"
            
        except Exception as e:
            print( 'Exception', e )
            LOG.debug( 'Invalid validation of token. {}'.format( str( e ) ) )
            raise BeaconServerError( error = 'Invalid validation of token. {}.'.format( str( e ) ) )

        if len( projects ) == 0:
            projects.append( 'no_project' )

        qparams = await process_request( request, entity )


        num_total_results, response = await fetch_func( qparams, access_token, groups, projects, request )

        # Create reponse
        #response_converted = build_beacon_response( entity, qparams, num_total_results, response, build_response_func )
        
        #Query parameters
        genomic_params = request.rel_url.query
        
        #Return directly the variant response
        if "v1" in str(request.url):
            response_converted = build_variant_v1_response( entity, qparams, num_total_results, response, build_response_func, genomic_params )
        else:
            response_converted = build_variant_response( entity, qparams, num_total_results, response, build_response_func )

        
        LOG.info( 'Formatting the response for %s', entity )
        return await json_response( request, response_converted )
    return wrapper

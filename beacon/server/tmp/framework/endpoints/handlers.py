#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import jwt
import logging

from server.config import config
from server.framework.utils import json_response
from server.framework.exceptions import  BeaconServerError, BeaconForbidden, BeaconEndPointNotImplemented
from server.framework.response import build_beacon_response
from server.gpap import get_kc_token


LOG         = logging.getLogger(__name__)
jwt_options = config.jwt_options
jwt_algorithm = config.jwt_algorithm
public_key  = '-----BEGIN PUBLIC KEY-----\n' + config.beacon_idrsa + '\n-----END PUBLIC KEY-----'

def test(entity):
    async def wrapper(request):
        LOG.debug('wrapper')
        response = {'result': 'this is a test'}
        return await json_response(request, response)
    return wrapper


def _extract_items(token,name):
    if (token.get(name)!=None):
        return [s.replace('/','') for s in token.get(name)]
    else:
        return []


# ('datasets' , _datasets_proxy, fetch_datsets_by_dataset, build_dataset_response)
def generic(entity, proxy, fetch_func, build_response_func):
    print('generic')
    async def wrapper(request):
        print('generic/wrapper')
        LOG.info('Running a request for {}'.format(entity))
        access_token = request.headers.get('Authorization')
        
        if not access_token and config.gpap_token_required[0]:
            LOG.debug('No access token but validation required.')
            raise BeaconForbidden(error = 'No authentication header was provided')
        elif not config.gpap_token_required[0]:
            LOG.debug('No access token and validation not required.')
            access_token = get_kc_token()['access_token']
        else:
            LOG.debug('Access token received.')
            access_token = access_token[7:]


        try:
            decoded  = jwt.decode(access_token, public_key, algorithms = jwt_algorithm, options = jwt_options)
            LOG.debug('Token was decoded')
            groups   = _extract_items(decoded,'group')
            projects = _extract_items(decoded,'group_projects')
        except Exception as e:
            print('Exception', e)
            LOG.debug('Invalid validation of token. {}'.format(str(e)))
            raise BeaconServerError(error = 'Invalida validation of token. {}.'.format(str(e)))

        if len(projects) == 0:
            projects.append("no_project")

        _, qparams = await proxy.fetch(request)
        LOG.debug(qparams)

        #######################################################################################
        # In RD-Connect each 'experiment' is a 'dataset', therfore it makes no sense to check
        # for dataset access since if the user asks for an individual or an experiment
        # that has no access GPAP returns empty.
        #######################################################################################
        non_accessible_datasets = []
        # datasets, authenticated = await resolve_token(access_token, qparams_db.datasetIds)
        # non_accessible_datasets = qparams_db.datasetIds - set(datasets)
        # LOG.debug('requested datasets:  %s', qparams_db.datasetIds)
        # LOG.debug('non_accessible_datasets: %s', non_accessible_datasets)
        # LOG.debug('resolved datasets:  %s', datasets)
        # if not datasets and non_accessible_datasets:
        #     error = f'You are not authorized to access any of these datasets: {non_accessible_datasets}'
        #     raise BeaconUnauthorised(error, api_error=proxy.api_error)

        num_total_results, response = fetch_func(qparams, access_token, groups, projects)
        
        # Create reponse
        #rows = [row async for row in response]
        #rows = [row for row in response]
        #num_total_results = await response_total_results
        response_converted = build_beacon_response(proxy, response, num_total_results, qparams, entity, non_accessible_datasets, build_response_func)

        print("hello response", response)
        
        LOG.info('Formatting the response for %s', entity)
        return await json_response(request, response_converted)
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
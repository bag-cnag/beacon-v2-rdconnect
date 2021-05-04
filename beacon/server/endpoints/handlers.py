#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import jwt
import logging
import datetime

from server.config import config
from server.utils.streamer import json_reponse
from server.utils.exceptions import BeaconEndPointNotImplemented, BeaconForbidden, BeaconServerError, BeaconUnauthorised

LOG         = logging.getLogger(__name__)
jwt_options = config.jwt_options
public_key  = '-----BEGIN PUBLIC KEY-----\n' + config.beacon_idrsa + '\n-----END PUBLIC KEY-----'

def extract_items(token,name):
    if (token.get(name)!=None):
        return [s.replace("/","") for s in token.get(name)]
    else:
        return []


def testing_handler(entity):
    async def wrapper(request):
        response = {'result': 'this is a test'}
        return await json_reponse(request, response)
    return wrapper

def not_implemented_handler(entity):
    async def wrapper(request):
        LOG.info('Running a request for %s (not implemented)', entity)
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
        raise BeaconEndPointNotImplemented() 
    return wrapper

def generic_handler(entity, by_entity_type, proxy, fetch_func, count_results_func, build_response_func):
    async def wrapper(request):
        LOG.info('Running a request for %s', entity)
        _, qparams_db = await proxy.fetch(request)
        LOG.debug(qparams_db)
        if LOG.isEnabledFor(logging.DEBUG):
            print_qparams(qparams_db, proxy, LOG)

        access_token = request.headers.get('Authorization')
        if access_token:
            access_token = access_token[7:] # cut out 7 characters: len('Bearer ')
            LOG.debug('---> access_token:  %s', access_token)
        else:
            LOG.debug('---> no access_token')

        datasets, authenticated = await resolve_token(access_token, qparams_db.datasetIds)
        non_accessible_datasets = qparams_db.datasetIds - set(datasets)

        LOG.debug('requested datasets:  %s', qparams_db.datasetIds)
        LOG.debug('non_accessible_datasets: %s', non_accessible_datasets)
        LOG.debug('resolved datasets:  %s', datasets)

        if not datasets and non_accessible_datasets:
            error = f'You are not authorized to access any of these datasets: {non_accessible_datasets}'
            raise BeaconUnauthorised(error, api_error=proxy.api_error)

        response = fetch_func(qparams_db, datasets, authenticated)
        response_total_results = count_results_func(qparams_db, datasets, authenticated)
        
        rows = [row async for row in response]
        num_total_results = await response_total_results

        # build_beacon_response knows how to loop through it
        response_converted = build_beacon_response(proxy, rows, num_total_results, qparams_db, by_entity_type, non_accessible_datasets, build_response_func)

        LOG.info('Formatting the response for %s', log_name)
        return await json_reponse(request, response_converted, partial=bool(non_accessible_datasets))
    return wrapper

def testing(entity):
    LOG.debug('hello!')
    async def wrapper(request):
        LOG.debug('wrapper')
        response = {'result': 'this is a test'}
        return await json_reponse(request, response)
    return wrapper

# Not implemented endpoints

individuals_by_biosample  = not_implemented_handler('individuals')
biosamples_by_biosample   = not_implemented_handler('biosamples')
gvariants_by_biosample    = not_implemented_handler('gvariants')

individuals_by_variant    = not_implemented_handler('individuals')
biosamples_by_variant     = not_implemented_handler('biosamples')
gvariants_by_variant      = not_implemented_handler('gvariants')

individuals_by_individual = not_implemented_handler('individuals')
biosamples_by_individual  = not_implemented_handler('biosamples')
gvariants_by_individual   = not_implemented_handler('gvariants')

cohorts_by_cohort         = not_implemented_handler('cohorts')

# Implemented endpoints

test  = testing_handler('test')

# individuals_by_biosample = generic_handler('individuals', BeaconEntity.BIOSAMPLE, individuals_proxy, db.fetch_individuals_by_biosample, db.count_individuals_by_biosample, build_biosample_or_individual_response)
# biosamples_by_biosample = generic_handler('biosamples' , BeaconEntity.BIOSAMPLE, biosamples_proxy , db.fetch_biosamples_by_biosample , db.count_biosamples_by_biosample, build_biosample_or_individual_response)
# gvariants_by_biosample = generic_handler('gvariants'  , BeaconEntity.BIOSAMPLE, gvariants_proxy  , db.fetch_variants_by_biosample   , db.count_variants_by_biosample, build_variant_response)

# individuals_by_variant = generic_handler('individuals', BeaconEntity.VARIANT, individuals_proxy, db.fetch_individuals_by_variant, db.count_individuals_by_variant, build_biosample_or_individual_response)
# biosamples_by_variant = generic_handler('biosamples' , BeaconEntity.VARIANT, biosamples_proxy , db.fetch_biosamples_by_variant , db.count_biosamples_by_variant, build_biosample_or_individual_response)
# gvariants_by_variant = generic_handler('gvariants'  , BeaconEntity.VARIANT, gvariants_proxy  , db.fetch_variants_by_variant   , db.count_variants_by_variant, build_variant_response)

# individuals_by_individual = generic_handler('individuals', BeaconEntity.INDIVIDUAL, individuals_proxy, db.fetch_individuals_by_individual, db.count_individuals_by_individual, build_biosample_or_individual_response)
# biosamples_by_individual = generic_handler('biosamples' , BeaconEntity.INDIVIDUAL, biosamples_proxy , db.fetch_biosamples_by_individual , db.count_biosamples_by_individual, build_biosample_or_individual_response)
# gvariants_by_individual = generic_handler('gvariants'  , BeaconEntity.INDIVIDUAL, gvariants_proxy  , db.fetch_variants_by_individual   , db.count_variants_by_individual, build_variant_response)

# cohorts_by_cohort = generic_handler('cohorts'  , BeaconEntity.COHORT, cohorts_proxy  , db.fetch_cohorts_by_cohort   , db.count_cohorts_by_cohort, build_cohort_response)

#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import jwt
import logging

from server.gpap import *
from server.config import config
from server.validation import BiosamplesParameters, GVariantsParameters, IndividualsParameters, CohortParameters
from server.utils.streamer import json_response
from server.utils.exceptions import BeaconEndPointNotImplemented, BeaconForbidden, BeaconServerError, BeaconUnauthorised
from server.endpoints.response.response_schema import *


LOG         = logging.getLogger(__name__)
jwt_options = config.jwt_options
jwt_algorithm = config.jwt_algorithm
public_key  = '-----BEGIN PUBLIC KEY-----\n' + config.beacon_idrsa + '\n-----END PUBLIC KEY-----'

def extract_items(token,name):
    if (token.get(name)!=None):
        return [s.replace("/","") for s in token.get(name)]
    else:
        return []


def testing_handler(entity):
    async def wrapper(request):
        response = {'result': 'this is a test'}
        return await json_response(request, response)
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

def generic_handler(entity, by_entity_type, proxy, fetch_func, build_response_func):
    async def wrapper(request):
        LOG.info('Running a request for %s', entity)
        access_token = request.headers.get('Authorization')
        if not access_token:
            raise BeaconForbidden(error = 'No authentication header was provided')

        access_token = access_token[7:]
        try:
            decoded  = jwt.decode(access_token, public_key, algorithms = jwt_algorithm, options = jwt_options)
            LOG.debug('Token was decoded')
            userid   = decoded.get('preferred_username')
            groups   = extract_items(decoded,'group')
            projects = extract_items(decoded,'group_projects')
        except Exception as e:
            LOG.debug('Invalida validation of token')
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
        #response_total_results = count_results_func(qparams, access_token, groups, projects)
        
        # Create reponse
        #rows = [row async for row in response]
        #rows = [row for row in response]
        #num_total_results = await response_total_results
        response_converted = build_beacon_response(proxy, response, num_total_results, qparams, by_entity_type, non_accessible_datasets, build_response_func)

        LOG.info('Formatting the response for %s', entity)
        return await json_response(request, response_converted)
    return wrapper

def testing(entity):
    async def wrapper(request):
        LOG.debug('wrapper')
        response = {'result': 'this is a test'}
        return await json_response(request, response)
    return wrapper

# Proxys in order to obtain the filtering criteria

biosamples_proxy  = BiosamplesParameters()
gvariants_proxy   = GVariantsParameters()
individuals_proxy = IndividualsParameters()
cohorts_proxy     = CohortParameters()

# Not implemented endpoints

individuals_by_biosample  = not_implemented_handler('individuals')
#biosamples_by_biosample   = not_implemented_handler('biosamples')
gvariants_by_biosample    = not_implemented_handler('gvariants')

individuals_by_variant    = not_implemented_handler('individuals')
biosamples_by_variant     = not_implemented_handler('biosamples')
gvariants_by_variant      = not_implemented_handler('gvariants')

#individuals_by_individual = not_implemented_handler('individuals')
#biosamples_by_individual  = not_implemented_handler('biosamples')
gvariants_by_individual   = not_implemented_handler('gvariants')

cohorts_by_cohort         = not_implemented_handler('cohorts')

# Implemented endpoints

test                      = testing_handler('test')

# individuals_by_biosample = generic_handler('individuals', BeaconEntity.BIOSAMPLE, individuals_proxy, fetch_individuals_by_biosample, build_biosample_or_individual_response)
biosamples_by_biosample = generic_handler('biosamples' , BeaconEntity.BIOSAMPLE, biosamples_proxy , fetch_biosamples_by_biosample, build_biosample_or_individual_response)
# gvariants_by_biosample = generic_handler('gvariants'  , BeaconEntity.BIOSAMPLE, gvariants_proxy  , fetch_variants_by_biosample, build_variant_response)

# individuals_by_variant = generic_handler('individuals', BeaconEntity.VARIANT, individuals_proxy, fetch_individuals_by_variant, build_biosample_or_individual_response)
# biosamples_by_variant = generic_handler('biosamples' , BeaconEntity.VARIANT, biosamples_proxy , fetch_biosamples_by_variant, build_biosample_or_individual_response)
# gvariants_by_variant = generic_handler('gvariants'  , BeaconEntity.VARIANT, gvariants_proxy  , fetch_variants_by_variant, build_variant_response)

individuals_by_individual = generic_handler('individuals', BeaconEntity.INDIVIDUAL, individuals_proxy, fetch_individuals_by_individual, build_biosample_or_individual_response)
biosamples_by_individual = generic_handler('biosamples' , BeaconEntity.INDIVIDUAL, biosamples_proxy , fetch_biosamples_by_individual, build_biosample_or_individual_response)
# gvariants_by_individual = generic_handler('gvariants'  , BeaconEntity.INDIVIDUAL, gvariants_proxy  , fetch_variants_by_individual, build_variant_response)

# cohorts_by_cohort = generic_handler('cohorts', BeaconEntity.COHORT, cohorts_proxy, fetch_cohorts_by_cohort, count_cohorts_by_cohort, build_cohort_response)

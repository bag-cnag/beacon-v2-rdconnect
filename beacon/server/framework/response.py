#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import logging
import json

from server.config import config
#from server.validation.fields import SchemaField
#from server.model.parameters import paramaters_to_entity
from server.framework.exceptions import BeaconServerError
from server.utils.request_origin import check_request_origin

LOG = logging.getLogger(__name__)

def handle_results_ranges(num_total_results):
    c_threshold = config.filters_in['counts_threshold']
    f_num_total_results = num_total_results

    if (num_total_results > 0) and (num_total_results < c_threshold):
        f_num_total_results = c_threshold - 1
    
    return f_num_total_results


def build_beacon_response( entity, qparams, num_total_results, data, build_response_func, all_data):

    print (all_data)
    
    #TO HANDLE
    #num_total_results = handle_results_ranges(num_total_results)

    num_total_results = sum(entry[key]['total'] for entry in all_data for key in entry)

    rst = { 
           'meta': build_meta( qparams ),
           'responseSummary': {
               'exists': True if num_total_results > 0 else False
           }
    }

    info = build_info(qparams)
    if info: rst['info'] = info

    if qparams[ 'query' ][ 'requestedGranularity' ] in ('count', 'record'):
        rst[ 'responseSummary' ][ 'numTotalResults' ] = num_total_results
        rst[ 'response' ] = build_response( entity, qparams, num_total_results, data, build_response_func, all_data )

    return rst

# def build_beacon_response(proxy, data, num_total_results, qparams_converted, entity, non_accessible_datasets, func_response_type):
#     """"
#     Transform data into the Beacon response format.
#     """
#     beacon_response = {
#         'meta': build_meta(proxy, qparams_converted, entity),
#         'response': build_response(data, num_total_results, qparams_converted, non_accessible_datasets, func_response_type, entity),
#         'responseSummary': { 'exists': True }
#     }
#     return beacon_response

def build_info(qparams):
    info = {}
    if "unsupportedFilters" in qparams[ 'query' ]:
        info["warnings"] = {}
        info["warnings"]["unsupportedFilters"] = qparams["query"]["unsupportedFilters"]

    return info 

def build_meta( qparams ):
    meta = {
        'beaconId': config.beacon_id,
        'apiVersion': config.api_version,
        #Currently we always return 'count'
        #'returnedGranularity': qparams[ 'query' ][ 'requestedGranularity' ],
        'returnedGranularity': 'count',
        #'receivedRequestSummary':  build_received_request_summary( qparams ),
        'returnedSchemas': qparams[ 'meta' ][ 'requestedSchemas' ],
    }
    return meta


# def build_received_request(entity, qparams):
#     request = {
#         'meta': {
#             'requestedSchemas' : qparams[ 'query' ][ 'requestedSchemas' ],
#             'apiVersion' : config.api_version,
#         },
#         'query': {} # build_received_query(qparams, entity),
#     }

#     return request

def build_received_request_summary( qparams ):
    request = {
        'apiVersion': qparams[ 'meta' ][ 'apiVersion' ],
        'requestedSchemas': qparams[ 'meta' ][ 'requestedSchemas' ],          
        #'filters': [qparams['query']['filters']],
        'requestedGranularity': qparams[ 'query' ][ 'requestedGranularity' ],
        'pagination': {
            'skip': qparams[ 'query' ][ 'pagination' ][ 'skip' ],
            'limit': qparams[ 'query' ][ 'pagination' ][ 'limit' ],
        }

        
        #Not needed according to meta section from Discovery Nexus
        #'pagination': {
        #    'skip': qparams[ 'query' ][ 'pagination' ][ 'skip' ],
        #    'limit': qparams[ 'query' ][ 'pagination' ][ 'limit' ],
        #},            
        #'requestParameters': {},            # TODO <--------
        #'includeResultsetResponses': 'HIT', # TODO <--------
        #'testMode': False                   # TODO <--------
    }
    return request


def build_received_query( entity, qparams ):
    query_part = {}
    if entity == 'datasets':
        build_datasets_filters( qparams )
    elif entity == 'individuals':
        pass
    elif entity == 'biosamples':
        pass
    else:
        raise BeaconServerError( 'Can not build response for entity "{}"'.format( entity ) )
    return query_part
    # g_variant  = None # build_g_variant_params(qparams, entity)
    # individual = None # build_individual_params(qparams, entity)
    # biosample  = None # build_biosample_params(qparams, entity)
    # datasets   = build_datasets_params(qparams)
    # pagination = build_pagination_params(qparams)

    # query_part = {}
    # if g_variant:
    #     query_part['g_variant']  = g_variant
    # if individual:
    #     query_part['individual'] = individual
    # if biosample:
    #     query_part['biosample']  = biosample
    # if datasets:
    #     query_part['datasets']   = datasets
    # if qparams.filters:
    #     query_part['filters']    = qparams.filters

    # return query_part


# # def build_g_variant_params(qparams, by_entity_type):
# #     """
# #     Fills the `gVariant` part with the request data
# #     """

# #     g_variant_params = {}
# #     if qparams.start:
# #         g_variant_params['start']          = qparams.start
# #     if qparams.end:
# #         g_variant_params['end']            = qparams.end
# #     if qparams.referenceBases:
# #         g_variant_params['referenceBases'] = qparams.referenceBases
# #     if qparams.alternateBases:
# #         g_variant_params['alternateBases'] = qparams.alternateBases
# #     if qparams.assemblyId:
# #         g_variant_params['assemblyId']     = qparams.assemblyId
# #     if qparams.referenceName:
# #         g_variant_params['referenceName']  = qparams.referenceName

# #     if by_entity_type == BeaconEntity.VARIANT and qparams.targetIdReq:
# #         g_variant_params['id']             = qparams.targetIdReq

# #     return g_variant_params

def build_datasets_filters( qparams ):
    datasets_params = {}
    if qparams[ 'parameters' ]:
        if type( qparams.id ) is list:
            datasets_params[ 'datasets' ] = qparams.id
        else:
            datasets_params[ 'datasets' ] = [ qparams.id ]
    
    return datasets_params

# # def build_individual_params(qparams, by_entity_type):
# #     """Fills the `individual` part with the request data"""

# #     individual_params = {}
# #     if by_entity_type == BeaconEntity.INDIVIDUAL and qparams.targetIdReq:
# #         individual_params['id'] = qparams.targetIdReq

# #     return individual_params


# # def build_biosample_params(qparams, by_entity_type):
# #     """
# #     Fills the `biosample` part with the request data
# #     """

# #     biosample_params = {}
# #     if by_entity_type == BeaconEntity.BIOSAMPLE and qparams.targetIdReq:
# #         biosample_params['id'] = qparams.targetIdReq

# #     return biosample_params


# def build_error(non_accessible_datasets):
#     """"
#     Fills the `error` part in the response.
#     This error only applies to partial errors which do not prevent the Beacon from answering.
#     """

#     message = f'You are not authorized to access some of the requested datasets: {non_accessible_datasets}'

#     return {
#         'error': {
#             'errorCode': 401,
#             'errorMessage': message
#         }
#     }


def build_resultSets_info(num_total_results):
    c_threshold = config.filters_in['counts_threshold']
    info = {}
    
    req_origin = check_request_origin()

    #EJP-related
    if (req_origin == "ejp") and (num_total_results > 0): 
        info["countType"] = "VCF file" 
        #info["contactPoint"] = "to_check" 
        #info["contactEmail"] = "to_check" 
        #info["contactURL"] = "to_check" 

    #Ranges
    resCountDesc =  'resultCountDescription' if req_origin == 'ejp' else 'resultsCountDescription'

    if (num_total_results > 0) and (num_total_results < c_threshold):
        info[resCountDesc] = {}
        info[resCountDesc]["minRange"] = 1
        info[resCountDesc]["maxRange"] = c_threshold - 1

    return info 


def build_response( entity, qparams, num_total_results, data, func, all_data ):

    req_origin = check_request_origin()

    resCount =  'resultCount' if req_origin == 'ejp' else 'resultsCount'
    resId =  'Unknown Zygosity' if entity == 'variants' else 'datasetBeacon'


    if entity == "variants" : entity = "genomicVariant"

    response = {
    'resultSets': []
    }

    # Iterate through all_data and add it to resultSets
    for data in all_data:
        for res_id, total_data in data.items():
            # Create the result set object
            result_set = {
                'id': res_id,
                'setType': entity,  # Adjust 'setType' as needed
                'exists': True if total_data['total'] > 0 else False,
                resCount: total_data['total'],
                'results': []  # Empty list for 'results' as per your structure
            }

            info = build_resultSets_info(total_data['total'])
            if info: result_set['info'] = info

            # Append to resultSets
            response['resultSets'].append(result_set)

    

    '''response = { 
        'resultSets': [ {
            'id': resId,
            'setType' : entity,
            'exists': True if num_total_results > 0 else False,
            resCount : num_total_results,
            'results': [],
            #'results': func( data, qparams )
            #'results': [{"info":"Currently only counts are returned"}] if num_total_results > 0 else []
            #Return actual results 'results': func( data, qparams ),

            #'info': build_resultSets_info(num_total_results)
            #'results':[], #'results': func( data, qparams ),
            # { 'description': '', '$ref': 'https://raw.githubusercontent.com/ga4gh-beacon/beacon-framework-v2/blob/main/common/beaconCommonComponents.json#/definitions/Info' },
            #'resultsHandover': [], # build_results_handover
            #'beaconHandover': config.beacon_handovers#,
        } ] }'''
    

    #In case of variants do not return ranges
    #if (entity != "variants"):
    #    info = build_resultSets_info(num_total_results)
    #    if info: response['resultSets'][0]['info'] = info


    #info = build_resultSets_info(num_total_results)
    #if info: response['resultSets'][0]['info'] = info

    return response


#Variants endpoint directly
def build_variant_response(entity, qparams, num_total_results, data, build_response_func):

    #Ranges also for variants
    num_total_results = handle_results_ranges(num_total_results)

    rst = { 
           'meta': build_meta( qparams ),
           'responseSummary': {
               'exists': True if num_total_results > 0 else False
           }
    }


    if qparams[ 'query' ][ 'requestedGranularity' ] in ('count', 'record'):
        rst[ 'responseSummary' ][ 'numTotalResults' ] = num_total_results
        rst[ 'response' ] = build_response( entity, qparams, num_total_results, data, build_response_func )

    return rst


#Variants with v1 response
def build_variant_v1_response(entity, qparams, num_total_results, data, build_response_func, genomic_params):


    #For Beacon v1 we have to return it in this format
    rst = {
        "beaconId": config.beacon_id,
        "apiVersion": "1.0.0",
        "exists": num_total_results > 0,
        "error": None,
        "alleleRequest": dict(genomic_params),
        "datasetAlleleResponses": [
            {
                "exists": num_total_results > 0,
                "variantCount": num_total_results,
                "callCount": num_total_results,
                "sampleCount": num_total_results,
                "note": "",
                "externalUrl": config.gpap_base_url + "/genomics/",
                "info": {"accessType":"ANONYMOUS"},
                "error": None
            }
        ]
    }


    return rst


# # def build_variant_response(data, qparams):
# #     """"
# #     Fills the `results` part with the format for variant data
# #     """

# #     variant_func = qparams.requestedSchema[1]
# #     variant_annotation_func = qparams.requestedAnnotationSchema[1]

# #     for row in data:
# #         yield {
# #             'variant': variant_func(row),
# #             'variantAnnotations': variant_annotation_func(row),
# #             'handovers': '',  # build_variant_handover
# #             'datasetAlleleResponses': row['dataset_response']
# #         }

# def build_dataset_response(data, qparams):
#     return data

# def build_biosample_or_individual_response(data, qparams):
#     """
#     Fills the `results` part with the format for biosample or individual data
#     """

#     # "$schema": "https://schemas-fake-depot.org/beaconv2/datasetSchema.json",
    
#     rsp = {
#         #"$schema": "https://raw.githubusercontent.com/ga4gh-beacon/beacon-framework-v2/main/responses/beaconCollectionsResponse.json",
#         #'meta': {
#         #    'beaconId':	'org.ga4gh.beacon',
#         #    'apiVersion': 'v2.0-draft4',
#         #    'returnedSchemas':	[	
#         #        { 'entryTypes': 'beacon-entry-types-v2.0.0-draft.4' }
#         #    ]
#         #},
#         #"receivedRequestSummary": {},
#         #"responseSummary": {
#         #    "exists": True
#         #},
#         #"resultSets":  [ qparams.requestedSchema[1](row) for row in data ]
#     }

#     rsp = [ qparams.requestedSchema[1](row) for row in data ]

#     return rsp

# # def build_cohort_response(data, qparams):
# #     return [qparams.requestedSchema[1](row) for row in data]
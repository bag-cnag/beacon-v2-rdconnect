#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import logging
import requests

from keycloak import KeycloakOpenID

from server.config import config
from server.gpap.payloads import *
from server.framework.exceptions import BeaconEndPointNotImplemented, BeaconForbidden, BeaconServerError, BeaconUnauthorised
from server.logger import LOG


def get_kc_token():
    keycloak_openid = KeycloakOpenID(
        server_url        = config.gpap_token_auth[ 'server_url' ],
        client_id         = config.gpap_token_auth[ 'client_id' ],
        realm_name        = config.gpap_token_auth[ 'realm_name' ],
        client_secret_key = config.gpap_token_auth[ 'client_secret_key' ],
        verify            = False
    )
    token = keycloak_openid.token( config.gpap_token_required[ 1 ], config.gpap_token_required[ 2 ] )
    return token


# Fetchers for GPAP's API

def _fetch_biosamples( qparams, access_token, groups ):

    #Check token
    token_status = check_token(access_token)

    if (token_status[1] == 200):

        headers = { 'Authorization': 'Token {}'.format( config.datamanagement_token ), 'Accept': 'application/json' }

        payload = datamanagement_playload( qparams, groups )
        url = config.gpap_base_url + config.dm_experiments

        resp = requests.post( url, headers = headers, data = json.dumps (payload ), verify = False )
        if resp.status_code != 200:
            raise BeaconServerError( error = resp.text )
        resp = resp.json()
        # print("==" * 20)
        # print("==" * 20)
        # print(resp[ 'items' ])
        # print("==" * 20)
        # print("==" * 20)
        return resp[ '_meta' ][ 'total_items' ], resp[ 'items' ]
    
    else:
        raise BeaconServerError( error = [ 'Authorization failed' ] )


#Common fetch for rest of the endpoints
def fetch_rest_by_type( qparams, access_token, groups, projects ):
    return 0, [ {
        'id': 'verifBeacon',
        'type': 'Fake abstracted level for beacon v2 implementation (in test)'
    } ]


def fetch_datsets_by_dataset( qparams, access_token, groups, projects ):
    return 1, [ {
        'id': 'datasetBeacon',
        'type': 'Fake abstracted level for beacon v2 implementation (in test)'
    } ]


# def fetch_biosamples_by_variant(qparams, access_token, groups, projects):
#     return 0, (x for x in [])

def fetch_biosamples_by_biosample(qparams, access_token, groups, projects):
    return _fetch_biosamples( qparams, access_token, groups )

#def fetch_biosamples_by_individual(qparams, access_token, groups, projects):
#    return _fetch_biosamples(qparams, access_token, groups)

#def fetch_variants_by_variant(qparams, access_token, groups, projects):
#    return 0, (x for x in [])

#def fetch_individuals_by_variant(qparams, access_token, groups, projects):
#    return 0, (x for x in [])

#def fetch_individuals_by_biosample(qparams, access_token, groups, projects):
#    return 0, (x for x in [])


def check_token(token):
    beacon_keys = config.beacon_keys
    keys_list = list(map(lambda x: x['key'], beacon_keys))

    if (config.gpap_token_required[0]):
        try:
            if (token in keys_list):
                userid = next(item["contact"] for item in beacon_keys if item["key"] == token)
                LOG.debug("#### Request submitted by: " + userid)
                return {'message': 'correct API key'}, 200

            else:
                LOG.debug('Request made with wrong token:' + token)
                return {'message': 'invalid API key'}, 401

        except Exception as e:
            LOG.debug('Something went wrong:' + str(e))
       
            return {'message': 'something went wrong '+str(e)}, 500

    else:
        LOG.debug('No Beacon key required')
        return {'message': 'no key required'}, 200



def fetch_individuals_by_individual( qparams, access_token, groups, projects ):
    payload = phenostore_playload( qparams, qparams[ 'targetIdReq' ] )
    
    #Check token
    token_status = check_token(access_token)

    if (token_status[1] == 200):
        headers = { 'Authorization_Beacon': config.pheno_token, 'Content-Type': 'application/json' }
        if qparams[ 'targetIdReq' ]:
            url = config.gpap_base_url + config.ps_participant.format( qparams[ 'targetIdReq' ] )
        else:
            url = config.gpap_base_url + config.ps_participants
        resp = requests.post( url, headers = headers, data = json.dumps( payload ), verify = False )

        if resp.status_code != 200:
            raise BeaconServerError( error = resp.json()[ 'message' ] )
        resp = json.loads( resp.text )

        return resp[ 'total' ], resp[ 'rows' ]
    
    else:
        raise BeaconServerError( error = [ 'Authorization failed' ] )



def fetch_variants_by_biosample( qparams, access_token, groups, projects ):
    return (x for x in [])

def fetch_variants_by_individual( qparams, access_token, groups, projects ):
    return (x for x in [])

def fetch_cohorts_by_cohort( qparams, access_token, groups, projects ):
    return (x for x in [])




'''Beacon v1 purposes'''
async def fetch_variants_by_variant( qparams, access_token, groups, projects, request ):
    #Check token
    token_status = check_token(access_token)
    
    #Do not check token for now as Beacon v1 was Public
    #if (token_status[1] == 200):

    
    #POST case
    if request.body_exists:
        req_body = await request.json()
        st_params = req_body["query"]["requestParameters"]

    #GET case
    else:
        st_params = request.rel_url.query

    
    #If no params are included set to arbitraty values for the Beacon verifier to pass    
    chrom = st_params.get('referenceName', '25')
    start = int(st_params.get("start", 0)) + 1
    ref = st_params.get('referenceBases', 'AB')
    alt = st_params.get('alternateBases', 'AB')

     
    #RefSeq chrom mapping, hg37
    if chrom.startswith("NC_") and chrom in config.filters_in['ref_seq_chrom_map_hg37']:
        chrom = config.filters_in['ref_seq_chrom_map_hg37'][chrom]
    

    if chrom == "MT":
        chrom = 23
    elif chrom == "X":
        chrom = 24
    elif chrom == "Y":
        chrom = 25
    else:
        pass

    variants_dict = {"chrom":chrom, "start":start, "ref":ref, "alt":alt}

    #print ("Fetch variants by variant")
    #print (variants_dict)

    #Elastic
    elastic_res = elastic_resp_handling(qparams, variants_dict)

    #variants_hits = elastic_res["datasetAlleleResponses"][0]["variantCount"]
    variants_hits = elastic_res

    #return resp[ 'total' ], resp[ 'rows' ]
    return variants_hits, variants_hits
    
    #else:
    #    raise BeaconServerError( error = [ 'Authorization failed' ] )

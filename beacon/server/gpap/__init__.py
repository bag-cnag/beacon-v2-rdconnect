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
#from app import create_history_entry
from server.db_model import History
import datetime


def get_kc_token_no_credentials():
    keycloak_openid = KeycloakOpenID(
        server_url=config.gpap_token_auth['server_url'],
        client_id=config.gpap_token_auth['client_id'],
        realm_name=config.gpap_token_auth['realm_name'],
        client_secret_key=config.gpap_token_auth['client_secret_key'],
        verify=False
    )

    # Use the client credentials grant type (no user credentials needed)
    token = keycloak_openid.token(grant_type="client_credentials")

    return token


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


def create_history_entry(request, entity_id, user_name, institution, content, res_status_code):
    history = History(
        entity_id=entity_id,
        timestamp = datetime.datetime.now(),
        username=user_name,
        groups=institution,
        endpoint=str(request.url),
        method=request.method,
        content=content,
        response_status_code = res_status_code

    )

    # Save the history entry to the database 
    with request.db.begin(): 
        request.db.add(history)
        request.db.commit()


def log_history(request, qparams, request_url, access_token, res_status_code):
    if res_status_code == 401:
        user_name = institution = "invalid_token"
    else:
        user_name = institution = "missing_token" 
    splitted = str(request_url).split("/")
    entity_id = splitted[len(splitted)-1] 
    content = dict(qparams) if request.method in ['POST', 'PUT'] else {} 

    create_history_entry(request, entity_id, user_name, institution, content, res_status_code)


# Fetchers for GPAP's API
def fetch_rest_by_type( qparams, access_token, groups, projects, request ):

    return [{'datasetBeacon': {'total': 0}}]
    '''return 0, [ {
        'id': 'verifBeacon',
        'type': 'Fake abstracted level for beacon v2 implementation (in test)'
    } ]'''


def fetch_biosamples_by_biosample(qparams, access_token, groups, projects, roles, request):

    if "variant_query_use" in roles:
        access_token = access_token['fixed_token']
    
    #Fixed token OR
    if config.fixed_token_use: 
        token_status = check_token(access_token)
    #Jwt token
    else:
        token_status = ['OK', 200]
    

    if (token_status[1] == 200):

        dm_responses = []

        for i in config.queries_endpoints:
            headers = { 'Authorization': 'Token {}'.format( i['dm_token'] ), 'Accept': 'application/json' }

            payload = datamanagement_playload( qparams, groups )

            print ("Projects are:")
            print (projects)

            #Add project filter for querying dataset OR no need since the project will be already in token?
            #Need to get projects from token
            #projects = ["CMS", "TreatHSP", "SolveRD"]
            #payload['filtered'].append({'id': "project", 'value': projects})
            #print (payload)
            
            resp = requests.post( i['url'] + config.dm_experiments, headers = headers, data = json.dumps( payload ), verify = False )

            if resp.status_code != 200:
                raise BeaconServerError( error = resp.text )
            resp = resp.json()
          
            #If call is made for g_variant query append experiment info
            if "variant_query_use" in roles:
                dm_responses = (resp['items'])
           
            else:
                # Granularity handling
                if "full_access" in roles:
                    dm_responses.append({i['entity']:{"total":resp['_meta']['total_items'], "rows":resp['items']}})
                else:
                    dm_responses.append({i['entity']:{"total":resp['_meta']['total_items']}})

         
        return dm_responses

        #Previously with one single endpoint
        '''headers = { 'Authorization': 'Token {}'.format( config.datamanagement_token ), 'Accept': 'application/json' }

        url = config.gpap_base_url + config.dm_experiments

        resp = requests.post( url, headers = headers, data = json.dumps (payload ), verify = False )
        if resp.status_code != 200:
            raise BeaconServerError( error = resp.text )
        resp = resp.json()
        return resp[ '_meta' ][ 'total_items' ], resp[ 'items' ]'''
    
    else:
        log_history(request, qparams, request.url, access_token, token_status[1])
        if token_status[1] == 401:
            raise BeaconUnauthorised( error = [ 'Invalid auth token' ] )
        else:
            raise BeaconServerError( error = [ 'No auth token provided' ] )


def fetch_individuals_by_individual( qparams, access_token, groups, projects, roles, request ):    

    #Fixed token OR
    if config.fixed_token_use: 
        token_status = check_token(access_token)
    #Jwt token
    else:
        token_status = ['OK', 200]

    print ("Projects are:")
    print (projects)

    print ("Groups are:")
    print (groups)

    print ("Roles are:")
    print (roles)


    if (token_status[1] == 200):

        ind_responses = []

        for i in config.queries_endpoints:
            
            #Fixed token for participants_fixed
            if config.fixed_token_use:
                headers = { 'Authorization-Beacon': i['pheno_token'], 'Content-Type': 'application/json' }
                ps_endpoint = config.ps_participants
                total_var = "total"

            #Keycloak token for participants_by_exp
            else:
                headers = { 'Authorization': access_token, 'Content-Type': 'application/json' }
                ps_endpoint = config.ps_participants_by_exp
                total_var = "total_page"

            payload = phenostore_playload( qparams, qparams[ 'targetIdReq' ] )

            #Add extra property to indicate that the query to participants_by_exp is for beacon purposes and filter by project there
            payload["beacon_query"] = True

            #Add project filter for querying dataset

            #If we add project field in PS
            #for p in projects:
            #    payload['filtered'].append({'id': "project", 'value': p})
            
            #for g in groups[0]:
            #    payload['filtered'].append({'id': "owner", 'value': g})

            resp = requests.post( i['url'] + ps_endpoint, headers = headers, data = json.dumps( payload ), verify = False )

            if resp.status_code != 200:
                raise BeaconServerError( error = resp.json()[ 'message' ] )
            
            resp = json.loads( resp.text )

            for r in (resp['rows']):
                print (r['id'])
             
            # Granularity handling
            if "full_access" in roles:
                ind_responses.append({i['entity']:{"total":resp[ 'total' ], "rows":resp['rows']}})
            else:
                ind_responses.append({i['entity']:{"total":resp[ total_var]}})
        
        #print (ind_responses)
        return ind_responses

        #Previously with one single endpoint
        '''headers = { 'Authorization-Beacon': config.pheno_token, 'Content-Type': 'application/json' }
        
        if qparams[ 'targetIdReq' ]:
            url = config.gpap_base_url + config.ps_participant.format( qparams[ 'targetIdReq' ] )
        else:
            url = config.gpap_base_url + config.ps_participants

        resp = requests.post( url, headers = headers, data = json.dumps( payload ), verify = False )

        if resp.status_code != 200:
            raise BeaconServerError( error = resp.json()[ 'message' ] )

        resp = json.loads( resp.text )

        return resp[ 'total' ], resp[ 'rows' ]'''
    
    else:
        log_history(request, qparams, request.url, access_token, token_status[1])
        if token_status[1] == 401:
            raise BeaconUnauthorised( error = [ 'Invalid auth token' ] )
        else:
            raise BeaconServerError( error = [ 'No auth token provided' ] )


'''Beacon v1 purposes'''
async def fetch_variants_by_variant( qparams, access_token, groups, projects, roles, request ):
    #Fixed token OR
    if config.fixed_token_use: 
        token_status = check_token(access_token['fixed_token'])
    #Jwt token
    else:
        token_status = ['OK', 200]            
    
    #Query DM for experiments to query
    experiments_to_query = []
    roles.append("variant_query_use")
    dm_experiments = fetch_biosamples_by_biosample( qparams, access_token, groups, projects, roles, request )
    for e in dm_experiments:
        if 'RD_Connect_ID_Experiment' in e:
            experiments_to_query.append(e['RD_Connect_ID_Experiment'])
        
    
    #Do not check token for now as Beacon v1 was Public
    if (token_status[1] == 200):

        variants_responses = []

        for i in config.queries_endpoints:

            #POST case
            if request.body_exists:
                req_body = await request.json()
                st_params = req_body["query"]["requestParameters"]

            #GET case
            else:
                st_params = request.rel_url.query

            
            #If no params are included set to arbitraty values for the Beacon verifier to pass    
            chrom = st_params.get('referenceName', '25')

            #Need to check (add 1 or get it as it is?)
            start = int(st_params.get("start", 0))
            #start = int(st_params.get("start", 0)) + 1
            
            ref = st_params.get('referenceBases', 'AB')
            alt = st_params.get('alternateBases', 'AB')
            assembly = st_params.get('assemblyId', None)


            #Handle assembly and chrom issues
            if assembly is not None and assembly != "GRCh37" and assembly != "hg19":
                raise BeaconServerError( error = [ 'Assembly id not found into database."' ] )

            #if assembly is not None and chrom.startswith("NC_"):
            #    raise BeaconServerError( error = [ 'Reference name should be in chr<Z> or <Z> notation (e.g. chr9 or 9)"' ] )

            if assembly is None and chrom not in config.filters_in['ref_seq_chrom_map_hg37']:
                raise BeaconServerError( error = [ 'Reference name or version not found into database.' ] )
    
            #RefSeq chrom mapping, hg37
            if chrom.startswith("NC_") and chrom in config.filters_in['ref_seq_chrom_map_hg37']:
                chrom = config.filters_in['ref_seq_chrom_map_hg37'][chrom]

            
            if chrom.startswith("chr"):
                chrom = chrom.split("chr")[1]

            if assembly is not None and chrom not in config.filters_in['ref_seq_chrom_map_hg37'].values():
                raise BeaconServerError( error = [ 'Invalid referenceName (chromosome) provided' ] )

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

            elastic_res = genomics_variants_resp_handling(qparams, access_token['service_token'], variants_dict, experiments_to_query)

            #Elastic
            #if config.fixed_token_use:
            #    elastic_res = elastic_resp_handling(qparams, variants_dict)
            #else:
            #    elastic_res = genomics_variants_resp_handling(qparams, access_token, variants_dict, experiments_to_query)

            #variants_hits = elastic_res["datasetAlleleResponses"][0]["variantCount"]
            variants_hits = elastic_res
             
            variants_responses = variants_hits
            #variants_responses.append({i['entity']:{"total":variants_hits}})
         
        return (variants_responses)
        #return resp[ 'total' ], resp[ 'rows' ]
        #return variants_hits, variants_hits

    else:
        log_history(request, qparams, request.url, access_token, token_status[1])
        if token_status[1] == 401:
            raise BeaconUnauthorised( error = [ 'Invalid auth token' ] )
        else:
            raise BeaconServerError( error = [ 'No auth token provided' ] )




'''Unused currently'''
#def fetch_biosamples_by_individual(qparams, access_token, groups, projects):
#    return _fetch_biosamples(qparams, access_token, groups)

#def fetch_variants_by_variant(qparams, access_token, groups, projects):
#    return 0, (x for x in [])

#def fetch_individuals_by_variant(qparams, access_token, groups, projects):
#    return 0, (x for x in [])

#def fetch_individuals_by_biosample(qparams, access_token, groups, projects):
#    return 0, (x for x in [])

# def fetch_biosamples_by_variant(qparams, access_token, groups, projects):
#     return 0, (x for x in [])

#def fetch_variants_by_biosample( qparams, access_token, groups, projects, request ):
#    return (x for x in [])

#def fetch_variants_by_individual( qparams, access_token, groups, projects ):
#    return (x for x in [])

#def fetch_cohorts_by_cohort( qparams, access_token, groups, projects ):
#    return (x for x in [])
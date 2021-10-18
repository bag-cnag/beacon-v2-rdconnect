#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import logging
import requests

from keycloak import KeycloakOpenID

from server.config import config
from server.gpap.payloads import *
from server.utils.exceptions import BeaconEndPointNotImplemented, BeaconForbidden, BeaconServerError, BeaconUnauthorised

LOG = logging.getLogger(__name__)


def get_kc_token():
    keycloak_openid = KeycloakOpenID(
        server_url        = config.gpap_token_auth['server_url'],
        client_id         = config.gpap_token_auth['client_id'],
        realm_name        = config.gpap_token_auth['realm_name'],
        client_secret_key = config.gpap_token_auth['client_secret_key'],
        verify            = False
    )
    token = keycloak_openid.token(config.gpap_token_required[1], config.gpap_token_required[2])
    return token


# Fetchers for GPAP's API

def _fetch_biosamples(qparams, access_token, groups):
    headers = { 'Authorization': 'Bearer {}'.format(access_token), 'Accept': 'application/json' }
    payload = datamanagement_playload(qparams, groups)
    url = config.gpap_base_url + config.dm_experiments

    resp = requests.post(url, headers = headers, data = json.dumps(payload), verify = False)
    if resp.status_code != 200:
        raise BeaconServerError(error = resp.text)
    resp = resp.json()
    return resp['_meta']['total_items'], resp['items']


def fetch_biosamples_by_variant(qparams, access_token, groups, projects):
    return (x for x in [])

def fetch_biosamples_by_biosample(qparams, access_token, groups, projects):
    return _fetch_biosamples(qparams, access_token, groups)

def fetch_biosamples_by_individual(qparams, access_token, groups, projects):
    return _fetch_biosamples(qparams, access_token, groups)

def fetch_variants_by_variant(qparams, access_token, groups, projects):
    return (x for x in [])

def fetch_individuals_by_variant(qparams, access_token, groups, projects):
    return (x for x in [])

def fetch_individuals_by_biosample(qparams, access_token, groups, projects):
    return (x for x in [])

def fetch_individuals_by_individual(qparams, access_token, groups, projects):
    payload = phenostore_playload(qparams, qparams.targetIdReq)
    headers = { 'Authorization': access_token, 'Content-Type': 'application/json' }
    if qparams.targetIdReq:
        #url = config.gpap_base_url + config.ps_participant.format(qparams.targetIdReq)
        url = config.gpap_base_url + config.ps_participants
    else:
        url = config.gpap_base_url + config.ps_participants
    resp = requests.post(url, headers = headers, data = json.dumps(payload), verify = False)

    if resp.status_code != 200:
        raise BeaconServerError(error = resp.json()['message'])
    resp = json.loads(resp.text)

    return resp['total'], resp['rows']

def fetch_variants_by_biosample(qparams, access_token, groups, projects):
    return (x for x in [])

def fetch_variants_by_individual(qparams, access_token, groups, projects):
    return (x for x in [])

def fetch_cohorts_by_cohort(qparams, access_token, groups, projects):
    return (x for x in [])



# # Counters for GPAP's API

# def count_variants_by_variant(qparams, access_token, groups, projects):
#     async def cnt():
#         return 0
#     return cnt()

# def count_variants_by_biosample(qparams, access_token, groups, projects):
#     async def cnt():
#         return 0
#     return cnt()

# def count_variants_by_individual(qparams, access_token, groups, projects):
#     async def cnt():
#         return 0
#     return cnt()

# def count_individuals_by_variant(qparams, access_token, groups, projects):
#     async def cnt():
#         return 0
#     return cnt()

# def count_individuals_by_biosample(qparams, access_token, groups, projects):
#     async def cnt():
#         return 0
#     return cnt()

# def count_individuals_by_individual(qparams, access_token, groups, projects):
#     async def cnt():
#         return 0
#     return cnt()

# def count_biosamples_by_variant(qparams, access_token, groups, projects):
#     async def cnt():
#         return 0
#     return cnt()

# def count_biosamples_by_biosample(qparams, access_token, groups, projects):
#     async def cnt():
#         return 0
#     return cnt()

# def count_biosamples_by_individual(qparams, access_token, groups, projects):
#     async def cnt():
#         return 0
#     return cnt()

# def count_cohorts_by_cohort(qparams, access_token, groups, projects):
#     async def cnt():
#         return 0
#     return cnt()
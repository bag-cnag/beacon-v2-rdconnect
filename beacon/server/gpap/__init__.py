#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import logging
import requests

from server.config import config
from server.gpap.payloads import *
from server.utils.exceptions import BeaconEndPointNotImplemented, BeaconForbidden, BeaconServerError, BeaconUnauthorised

LOG = logging.getLogger(__name__)

def close_session():
    session.close()

# Fetchers for GPAP's API

def fetch_biosamples_by_variant(qparams, access_token, groups, projects):
    return (x for x in [])

def fetch_biosamples_by_biosample(qparams, access_token, groups, projects):
    return (x for x in [])

def fetch_biosamples_by_individual(qparams, access_token, groups, projects):
    return (x for x in [])

def fetch_variants_by_variant(qparams, access_token, groups, projects):
    return (x for x in [])

def fetch_individuals_by_variant(qparams, access_token, groups, projects):
    return (x for x in [])

def fetch_individuals_by_biosample(qparams, access_token, groups, projects):
    return (x for x in [])

def fetch_individuals_by_individual(qparams, access_token, groups, projects):
    payload = phenostore_playload(qparams)
    headers = { 'Authorization': access_token, 'Content-Type': 'application/json' }
    if qparams.targetIdReq:
        url = config.gpap_base_url + config.ps_participant.format(qparams.targetIdReq)
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
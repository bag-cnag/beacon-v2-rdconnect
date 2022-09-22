#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import requests
from server.config import config

# THE FOLLWING ARE THREE HELPER FUNCTION TO TEST FOR ANSWER STRUCTURE

def _check_meta_(cnt):
    _keys = ['beaconId', 'apiVersion', 'receivedRequest', 'returnedSchemas']
    if 'meta' in cnt.keys():
        return sum([ x in cnt['meta'].keys() for x in _keys]) == len(_keys)
    return False

def _check_response_(cnt):
    _keys = ['exists', 'numTotalResults', 'results', 'info', 'resultsHandover', 'beaconHandover']
    if 'response' in cnt.keys():
        return sum([ x in cnt['response'].keys() for x in _keys]) == len(_keys)
    return False

_keys_biosambles = ['biosampleId', 'subjectId', 'description', 'biosampleStatus', 'collectionDate', 'subjectAgeAtCollection', 'sampleOriginDescriptors', 'obtentionProcedure', 'cancerFeatures', 'handovers', 'info']
_keys_individual = ['individualId', 'taxonId', 'sex', 'ethnicity', 'geographicOrigin', 'phenotypicFeatures', 'diseases', 'pedigrees', 'handovers', 'treatments', 'interventions', 'measures', 'exposures', 'info']
def _check_response_results_(cnt, _keys):
    return sum([ x in cnt.keys() for x in _keys]) == len(_keys)

# HERE WE TEST FOR THE LIST ENPOINTS AND SEE IF THE RESPONSE
# FOLLOWS THE DESIRED STRUCTURE

def test_biosamples_list(token):
    headers = {'Authorization': 'Bearer {}'.format(token)}
    url = '{}/api/biosamples'.format(config.server_api_url)
    rsp = requests.post(url, headers = headers, verify = False)
    cnt = json.loads(rsp.text)
    assert rsp.status_code == 200
    assert _check_meta_(cnt)
    assert _check_response_(cnt)
    assert cnt['response']['numTotalResults'] > 0
    assert _check_response_results_(cnt['response']['results'][0], _keys_biosambles)

def test_individuals_list(token):
    headers = {'Authorization': 'Bearer {}'.format(token)}
    url = '{}/api/individuals'.format(config.server_api_url)
    rsp = requests.post(url, headers = headers, verify = False)
    cnt = json.loads(rsp.text)
    assert rsp.status_code == 200
    assert _check_meta_(cnt)
    assert _check_response_(cnt)
    assert cnt['response']['numTotalResults'] > 0
    assert _check_response_results_(cnt['response']['results'][0], _keys_individual)

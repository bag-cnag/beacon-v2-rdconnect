#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import requests
from server.config import config


# THE FOLLIWING ARE THE TEST FOR THE IMPLEMENTED ENDPOINTS
# THE FIRST SET TESTS THE LISTING ENDPOINTS EXPECTING 200 AS
# RESULTS AND SOME CONTENT (EXISTS TRUE AND NUMBER OF RESULTS
# OVER ZERO)

#Content-type constant
content_type = 'application/json'


'''def test_biosamples_list(token):
    headers = {'Authorization': 'Bearer {}'.format(token)}
    url = '{}/api/biosamples'.format(config.server_api_url)
    rsp = requests.post(url, headers = headers, verify = False)
    cnt = json.loads(rsp.text)
    assert rsp.status_code == 200
    assert cnt['response']['exists']
    assert cnt['response']['numTotalResults'] > 0
    assert len(cnt['response']['results']) > 0

def test_individuals_list(token):
    headers = {'Authorization': 'Bearer {}'.format(token)}
    url = '{}/api/individuals'.format(config.server_api_url)
    rsp = requests.post(url, headers = headers, verify = False)
    cnt = json.loads(rsp.text)
    assert rsp.status_code == 200
    assert cnt['response']['exists']
    assert cnt['response']['numTotalResults'] > 0
    assert len(cnt['response']['results']) > 0

# THE SECOND TEST QUERIES FIRST THE LIST AND THEN USES THE
# INDIVIDUAL ENDPOINT TO QUERY FOR A SINGLE RESULT

def test_biosamples_biosample(token):
    headers = {'Authorization': 'Bearer {}'.format(token)}
    url = '{}/api/biosamples'.format(config.server_api_url)
    rsp = requests.post(url, headers = headers, verify = False)
    cnt = json.loads(rsp.text)
    print(cnt)
    ind = cnt['response']['results'][0]['biosampleId']
    url = '{}/api/biosamples/{}'.format(config.server_api_url, ind)
    rsp = requests.post(url, headers = headers, verify = False)
    cnt = json.loads(rsp.text)
    assert rsp.status_code == 200
    assert cnt['response']['exists']
    assert cnt['response']['numTotalResults'] == 1
    assert len(cnt['response']['results']) == 1
    assert  cnt['response']['results'][0]['biosampleId'] == ind'''

def test_individuals_endpoint():
    token = config.beacon_keys[0]['key']
    headers = {'Content-Type': content_type, 'auth-key': token}
    
    url = '{}/api/individuals'.format(config.server_api_url)
     

    data = {
    "meta": {
        "apiVersion": "v0.2",
        "requestedSchemas": [
            {
                "entityType": "Individual",
                "schema": "https://raw.githubusercontent.com/ga4gh-beacon/beacon-v2/main/models/json/beacon-v2-default-model/individuals/defaultSchema.json"
            }
        ]
    },
    "query": {
        "filters": [
        	    {
                      "id":["ordo:Orphanet_778", "ordo:Orphanet_140162"]
                },
                
                {
                      "id":["obo:HP_0002086","hp_0045026","HP_0000316"]
                },
                
                {
                      "id": "obo:NCIT_C28421",
                      "value": "NCIT_C20197",
                      "operator": "="
                },
          
                {
                      "id":"obo:NCIT_C83164",
                      "value":"50",
                      "operator":"="
                },
                {
                      "id":"obo:NCIT_C124353",
                      "value":"20",
                      "operator":"="

                },
                {
                      "id":"obo:NCIT_C156420",
                      "value":"25",
                      "operator":"="
                }
        ]
      }
    }


    rsp = requests.post(url, data = json.dumps(data), headers = headers, verify = False)
    cnt = json.loads(rsp.text)
    assert rsp.status_code == 200
    assert cnt['responseSummary']['exists'] == True
    assert cnt['responseSummary']['numTotalResults'] == 9

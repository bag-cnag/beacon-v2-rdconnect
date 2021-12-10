#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import requests
from server.config import config

# THE FOLLIWING ARE THE TEST FOR THE IMPLEMENTED ENDPOINTS
# THE FIRST SET TESTS THE LISTING ENDPOINTS EXPECTING 200 AS
# RESULTS AND SOME CONTENT (EXISTS TRUE AND NUMBER OF RESULTS
# OVER ZERO)

def test_biosamples_list(token):
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
    assert  cnt['response']['results'][0]['biosampleId'] == ind

def test_individuals_individual(token):
    headers = {'Authorization': 'Bearer {}'.format(token)}
    url = '{}/api/individuals'.format(config.server_api_url)
    rsp = requests.post(url, headers = headers, verify = False)
    cnt = json.loads(rsp.text)
    ind = cnt['response']['results'][0]['individualId']
    url = '{}/api/individuals/{}'.format(config.server_api_url, ind)
    rsp = requests.post(url, headers = headers, verify = False)
    cnt = json.loads(rsp.text)
    assert rsp.status_code == 200
    assert cnt['response']['exists']
    assert cnt['response']['numTotalResults'] == 1
    assert len(cnt['response']['results']) == 1
    assert cnt['response']['results'][0]['individualId'] == ind
